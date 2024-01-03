import discord
import asyncio
import pickle
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = discord.Client(intents=intents)



async def fetch_messages():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            print(f"Logged in as {client.user}")
            # --- LIST GUILDS ---
            print("Select a guild to inspect interactions:")
            for idx, guild in enumerate(client.guilds, start=1):
                print(f"{idx}. {guild.name}")

            guild_choice = int(
                input("Enter the number of the guild you want to inspect: ")
            )
            guild = client.guilds[guild_choice - 1]
            print(f"Selected guild: {guild.name}")
            if not guild:
                raise Exception(f"Guild error: {guild.name} not found")
            # --- IDENTIFY USER ---
            # Retrieve all users in the server
            users = [member for member in guild.members if not member.bot]

            print("Select a user to inspect interactions:")
            for idx, user in enumerate(users, start=1):
                print(f"{idx}. {user.name}")

            user_choice = int(
                input("Enter the number of the user you want to inspect: ")
            )
            selected_user = users[user_choice - 1]
            print(f"Selected user: {selected_user.name}")
            selected_user_id = selected_user.id

            interactions = []
            print("Looking through channels for interaction history...")
            for channel in guild.channels:
                print(f"looking at channel {channel.name}")
                if isinstance(channel, discord.TextChannel):
                    # oldest_first needs to be set so that history is preserved
                    async for message in channel.history(limit=None, oldest_first=True):
                        # make sure the message is from the selected user
                        if message.author.id != selected_user_id:
                            continue
                        reference = message.reference
                        # make sure this is a reply to a message in the same channel
                        if not (
                            reference
                            and reference.message_id
                            and reference.channel_id == channel.id
                            and reference.resolved
                            and not isinstance(
                                reference.resolved, discord.DeletedReferencedMessage
                            )
                        ):
                            continue
                        # make sure the message is a reply to a different user
                        if message.author.id == reference.resolved.author.id:
                            continue
                        # make sure the message is not a reply to a bot
                        if reference.resolved.author.bot:
                            continue
                        # If there is no text in the message or the response, skip it
                        # This is to avoid looking at responses to images, etc.
                        if (
                            not message.clean_content
                            or not reference.resolved.clean_content
                        ):
                            continue

                        interactions.append(
                            {
                                "id": message.id,
                                "response": message.clean_content,
                                "message": reference.resolved.clean_content,
                            }
                        )

            # Save the interactions to a file with the user's name and guild name
            with open(
                f"{selected_user.name}_interactions_in_{guild.name}.pkl", "wb"
            ) as file:
                pickle.dump(interactions, file)
            print(interactions)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await client.close()

    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    try:
        await client.start(BOT_TOKEN)
    except discord.LoginFailure as e:
        print(f"Failed to log in: {e}")


async def main():
    await fetch_messages()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
