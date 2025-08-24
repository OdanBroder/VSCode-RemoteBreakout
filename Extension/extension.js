const vscode = require('vscode');

function activate(context) {
    vscode.window.showInformationMessage("Local Terminal Remote Extension Activated");

    const disposable = vscode.commands.registerCommand('sendCommand', async () => {
        // Open a new local terminal
        await vscode.commands.executeCommand('workbench.action.terminal.newLocal');

        // Get active terminal (should now exist)
        const terminal = vscode.window.activeTerminal;
        let command = "echo Hacked";

        if (terminal) {
            // Send text + execute (true = press Enter)
            terminal.sendText(command, true);
        } else {
            vscode.window.showErrorMessage("No active terminal found.");
        }
    });

    context.subscriptions.push(disposable);

    vscode.commands.executeCommand('sendCommand');
}

function deactivate() {
    vscode.window.showInformationMessage("Local Terminal Remote Extension Deactivated");
}

module.exports = {
    activate,
    deactivate
};
