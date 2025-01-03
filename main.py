from pyrogram import Client, filters
import requests

# Bot Configuration
API_ID = "28255147"  # Replace with your Telegram API ID
API_HASH = "8113960fe67c0cc815e6acce2aefb410"  # Replace with your Telegram API Hash
BOT_TOKEN = "7909567101:AAHU1b-o0L94Jf7RHZTmcdeRa8PJdTrost0"  # Replace with your Telegram bot token
GITHUB_TOKEN = "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"  # Replace with your GitHub personal access token

# Admins List
ADMIN_IDS = [1110013191, 6663845789]  # Replace with Telegram user IDs of authorized admins

app = Client("github_repo_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# GitHub API headers
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def toggle_repo_visibility(owner, repo, visibility):
    """
    Toggles the visibility of a GitHub repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.patch(url, headers=HEADERS, json={"private": visibility})
    
    if response.status_code == 200:
        return {"success": True, "message": "Repository visibility updated successfully."}
    else:
        error_message = response.json().get("message", "Unknown error")
        return {
            "success": False,
            "status_code": response.status_code,
            "error": error_message,
        }

@app.on_message(filters.command("toggle") & filters.private)
async def toggle_repo(client, message):
    """
    Command to toggle GitHub repo visibility.
    Usage: /toggle <owner/repo> <public|private>
    """
    # Check if the user is an admin
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not authorized to use this bot.")
        return
    
    if len(message.command) != 3:
        await message.reply("Usage: /toggle <owner/repo> <public|private>")
        return
    
    repo_info, visibility = message.command[1], message.command[2].lower()
    if visibility not in ["public", "private"]:
        await message.reply("Visibility must be either 'public' or 'private'.")
        return
    
    try:
        owner, repo = repo_info.split("/")
    except ValueError:
        await message.reply("Invalid repository format. Use: <owner/repo>.")
        return
    
    visibility_flag = True if visibility == "private" else False
    result = toggle_repo_visibility(owner, repo, visibility_flag)
    
    if result["success"]:
        await message.reply(f"Repository `{repo_info}` successfully updated to `{visibility}`.")
    else:
        await message.reply(
            f"Failed to update repository:\n"
            f"Error: {result['error']} (HTTP {result['status_code']})"
        )

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    """
    /start command handler.
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not authorized to use this bot.")
        return
    
    await message.reply(
        "Welcome to the GitHub Repo Visibility Bot!\n\n"
        "Commands:\n"
        "/toggle <owner/repo> <public|private> - Toggle a repo's visibility"
    )

if __name__ == "__main__":
    app.run()
