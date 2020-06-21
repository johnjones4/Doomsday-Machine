(async () => {
  const chartWidth = window.innerWidth
  const chartHeight = window.innerHeight * 0.7
  const chartMargin = 0
  const chartRadius = Math.min(chartWidth, chartHeight) / 2 - chartMargin

  const loadData = async () => {
    const response = await fetch('/api/status')
    return await response.json()
  }

  const drawChart = (jobs) => {
    d3.select("#chart").selectAll("*").remove();
    
    const svg = d3.select("#chart")
      .append("svg")
      .attr("width", chartWidth)
      .attr("height", chartHeight)
      .append("g")
      .attr("transform", "translate(" + chartWidth / 2 + "," + chartHeight / 2 + ")")

    const color = d3.scaleLinear()
      .domain([0,jobs.length - 1])
      .range([100,200])

    const blueColor = d3.scaleLinear()
      .domain([0,jobs.length - 1])
      .range([150,250])

    const jobSeconds = d => {
      if (d.last_execution_time) {
        return d.last_execution_time
      } else if (d.start_time) {
        return (new Date().getTime() / 1000) - d.start_time
      } else {
        return 0
      }
    }

    const formatTime = t => {
      if (t < 60) {
        return `${Math.round(t)} Seconds`
      } else if (t < 3600) {
        return `${Math.round(t / 60)} Minutes`
      } else if (t < 216000) {
        return `${Math.round(t / 60 / 60)} Hours`
      } else {
        return `${Math.round(t / 60 / 60 / 24)} Days`
      }
    }
    
    const pie = d3.pie()
      .value(d => Math.log(jobSeconds(d)))
    
    const dataReady = pie(jobs)

    const arc = d3.arc()
      .innerRadius(chartRadius * 0.4)
      .outerRadius(chartRadius * 0.8)

    const outerArc = d3.arc()
      .innerRadius(chartRadius * 0.9)
      .outerRadius(chartRadius * 0.9)

    svg
      .selectAll('slices')
      .data(dataReady)
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('class', (d) => ['pie-segment', 'pie-segment-' + (!isNaN(d.data.start_time) && d.data.start_time > 0 ? 'active' : 'inactive')].join(' '))
      .attr('fill',(d,i) => `rgb(${color(i)},${color(i)},${blueColor(i)})`)

    svg
      .selectAll('lines')
      .data(dataReady)
      .enter()
      .append('polyline')
      .attr('class', 'label-line')
      .attr('points', (d) => {
        const posA = arc.centroid(d)
        const posB = outerArc.centroid(d)
        const posC = outerArc.centroid(d)
        const midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
        posC[0] = chartRadius * 0.95 * (midangle < Math.PI ? 1 : -1)
        return [posA, posB, posC]
      })
    
    svg
      .selectAll('labels')
      .data(dataReady)
      .enter()
      .append('text')
      .text(d => `${d.data.name} (${formatTime(jobSeconds(d.data))})`)
      .attr('class', 'label')
      .attr('transform', function(d) {
        const pos = outerArc.centroid(d);
        const midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
        pos[0] = chartRadius * 0.99 * (midangle < Math.PI ? 1 : -1);
        return 'translate(' + pos + ')';
      })
      .style('text-anchor', function(d) {
        const midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
        return (midangle < Math.PI ? 'start' : 'end')
      })
  }

  const { jobs } = await loadData()
  drawChart(jobs)

  setInterval(async () => {
    const { jobs } = await loadData()
    drawChart(jobs)
  }, 5000)
})()
