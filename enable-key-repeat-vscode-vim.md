```bash
    defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
    osascript -e 'tell application "Visual Studio Code" to quit'
    osascript -e 'tell application "Visual Studio Code" to activate'
```
