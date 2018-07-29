const express = require('express')
const CronJob = require('cron').CronJob
const { spawn } = require('child_process')
const jobs = [
  {
    name: 'lastpass',
    label: 'LastPass',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'imap',
    label: 'IMAP',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'evernote',
    label: 'Evernote',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'rclone',
    label: 'RClone',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'googlecontacts',
    label: 'Google Contacts',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'todoist',
    label: 'Todoist',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'github',
    label: 'GitHub',
    running: false,
    log: '',
    started: null
  },
  {
    name: 'archive',
    label: 'Archive',
    running: false,
    log: '',
    started: null
  }
]

const startServer = () => {
  const app = express()
  app.set('view engine', 'ejs')

  app.get('/', (req, res) => {
    res.render('index', {
      jobs
    })
  })

  app.get('/job/:job', (req, res) => {
    const job = jobs.find(job => job.name === req.params.job)
    res.render('job', {
      job
    })
  })

  app.listen(process.env.PORT || 80)
}

const startJob = (job) => {
  if (!job.running) {
    job.running = true
    job.log = ''
    job.started = new Date().getTime()
    subProcess = spawn('/scripts/' + job.name + '.sh')
    subProcess.on('close', () => {
      job.running = false
      job.started = null
    })
    subProcess.stdout.on('data', (data) => {
      job.log += data
    })
    subProcess.stderr.on('data', (data) => {
      job.log += data
    })
  }
}

const startJobTimers = () => {
  jobs.forEach((job, i) => {
    let cronjob = new CronJob(
      '0 ' + i + ' * * *',
      () => startJob(job),
      null,
      true,
      'America/New_York'
    )
    if (cronjob.running) {
      console.log(job.name + ' setup')
    }
  })
}

startJobTimers()
startServer()