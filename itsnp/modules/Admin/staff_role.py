from datetime import datetime

import hikari
import tanjun

from itsnp.core.client import Client
from models import ModerationRoles

from . import role_group

staff_role_component = tanjun.Component()


@role_group.with_command
@tanjun.with_own_permission_check(
    hikari.Permissions.SEND_MESSAGES
    | hikari.Permissions.VIEW_CHANNEL
    | hikari.Permissions.EMBED_LINKS
)
@tanjun.with_role_slash_option("role", "Role or role id of staff role")
@tanjun.as_slash_command("staff", "Set staff role for the server.")
async def staff_role_command(ctx: tanjun.abc.Context, role: hikari.Role) -> None:
    guild = ctx.get_guild()
    model, _ = await ModerationRoles.get_or_create(guild_id=ctx.guild_id)
    model.staff_role = role.id
    await model.save()
    embed = hikari.Embed(
        title="Staff Role",
        description=f"The staff role  for {guild.name} has been set to {role.mention}",
        timestamp=datetime.now().astimezone(),
        color=hikari.Color(0x00FF00),
    )
    await ctx.respond(embed=embed)


@tanjun.as_loader
def load_components(client: Client):
    client.add_component(staff_role_component.copy())
