const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    },
    icon: path.join(__dirname, 'build/icon.png')
  });

  mainWindow.loadFile('index.html');

  // Open DevTools in development mode
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Handle file opening
ipcMain.handle('open-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'All Supported Files', extensions: ['pdf', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'bmp'] },
      { name: 'PDF Files', extensions: ['pdf'] },
      { name: 'Text Files', extensions: ['txt'] },
      { name: 'Images', extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });

  if (!result.canceled && result.filePaths.length > 0) {
    const filePath = result.filePaths[0];
    const ext = path.extname(filePath).toLowerCase();
    
    if (ext === '.pdf') {
      // Read PDF as buffer
      const buffer = fs.readFileSync(filePath);
      return {
        type: 'pdf',
        data: buffer.toString('base64'),
        name: path.basename(filePath)
      };
    } else if (ext === '.txt') {
      // Read text file
      const content = fs.readFileSync(filePath, 'utf-8');
      return {
        type: 'text',
        data: content,
        name: path.basename(filePath)
      };
    } else if (['.jpg', '.jpeg', '.png', '.gif', '.bmp'].includes(ext)) {
      // Read image file
      const buffer = fs.readFileSync(filePath);
      const mimeType = ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : 
                       ext === '.png' ? 'image/png' :
                       ext === '.gif' ? 'image/gif' : 'image/bmp';
      return {
        type: 'image',
        data: `data:${mimeType};base64,${buffer.toString('base64')}`,
        name: path.basename(filePath)
      };
    }
  }
  
  return null;
});
