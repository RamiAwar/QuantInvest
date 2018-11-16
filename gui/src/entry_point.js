const electron = require('electron')
const _window = require('./common/window.js');

// DEV ONLY - AUTOMATED RELOAD
require('electron-reload')(__dirname, {
    // Note that the path to electron may vary according to the main file
    electron: require(`${__dirname}/../node_modules/electron`)
});


const app = electron.app  // Module to control application life.
const BrowserWindow = electron.BrowserWindow  // Module to create native browser window.

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let main_window = null;


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.on('ready', function(){
	main_window = _window.create_window('../views/html/loader_window.html', 800, 600);
});

// Quit when all windows are closed.
app.on('window-all-closed', function() {

  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform != 'darwin') {
    app.quit();
  }

  // But OS X can be annoying so:
  app.quit();
  // Will decide whether or not to remove this upon further usage
  
});
