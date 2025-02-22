module.exports = {
  appId: 'com.truedownloadmanager.app',
  productName: 'True Download Manager',
  directories: {
    output: 'dist',
    buildResources: 'build'
  },
  files: [
    'main.js',
    '../frontend/dist/**/*'
  ],
  win: {
    target: [
      {
        target: 'nsis',
        arch: ['x64']
      }
    ]
  },
  mac: {
    target: 'dmg',
    category: 'public.app-category.utilities'
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true
  }
}