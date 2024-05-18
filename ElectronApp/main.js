const {app, BrowserWindow, globalShortcut, dialog, Tray, Menu} = require('electron');
const windowStateKeeper = require('electron-window-state');
console.warn("Main Process is running");
function createWindow(){
    let mainWindowState = windowStateKeeper({
      defaultWidth:800,
      defaultHeight:500
    });
    let win = new BrowserWindow({
      x:mainWindowState.x,
      y:mainWindowState.y,
      width:mainWindowState.width,
      height:mainWindowState.height,
      // frame : false,// make frame fixed
      alwaysOnTop : false,
      title: "Awesome App",
      backgroundColor: "#ff0000",
      webPreferences:{
        nodeIntegration : true
      }
  });

  // let child = new BrowserWindow({parent:win});
  // child.loadFile("child.html");
  // child.show();
  mainWindowState.manage(win);
  win.loadFile("index.html");
  win.webContents.openDevTools();
  let wc = win.webContents;
  wc.on('dom-ready',()=>{
    console.log('dom is ready');
  });
  wc.on('did-finish-load',()=>{
    console.log('did finish load');
  });
  wc.on('new-window',()=>{
    console.log('new window opened');
  });
  wc.on('before-input-event',()=>{
    console.log('some key is pressed');
  });
  globalShortcut.register("shift+k",()=>{
    console.log("shift+k key is pressed");
    dialog.showOpenDialog({
      defaultPath:app.getPath('desktop'),
      buttonLabel: 'select file'
    });
  })
  tray = new Tray('pic.png');
  tray.setToolTip('tray to electron app')
  tray.on('click',()=>{
    win.isVisible()?win.hide():win.show();
  })
  let template = [{label : 'item1', type : 'radio'},{label : 'item2'}];
  let menuTEmplate = [
    {label:'blog',submenu:[{label:'about'},{label:'vision'}]},
    {label:'file'},
    {label:'operation',submenu:[{label : 'close',role:'quit'},{label:'zoom'}]}
  ];
  let menu = Menu.buildFromTemplate(menuTEmplate);
  Menu.setApplicationMenu(menu);
  const contexMenu = Menu.buildFromTemplate(template);
  tray.setContextMenu(contexMenu);
}
// app.whenReady().then(createWindow);
app.on('before-quit',(e)=>{
  console.log('call before quit app');
});
app.on('will-quit',(e)=>{
  console.log('call will quit app');
});
app.on('browser-window-focus',()=>{
  console.log('you are on the app');
});
app.on('browser-window-blur',()=>{
  console.log('you are unfocus app');
});
app.on('ready',()=>{
  createWindow();
  console.log('app init');
});
