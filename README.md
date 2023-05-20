# ezPaint
A Blender add-on that allows for easy weightpainting of models from SW:TOR, Jedi Knight II, Jedi Academy, Star Wars Jedi Series, the Battlefront Series, and Destiny 2. You can also load custom settings for vertex groups and merges!
After the automatic weightpaint, you will need to export as SMD, and compile the model using a proportioned skeleton.
# How to Use:
## Step 1: Install as a Blender addon


## Custom file demo:
https://github.com/FallenLogic/ezPaint/assets/68028253/b829450d-d7ff-4a9a-b44c-827266778dad
For a custom vertex group mapping file,
The first line must be a number (this is converted to a float or int), and it is the scaling factor applied to the active object when the custom file is applied. If the object is in the correct scale, simply make the first line the number 1.

For vertex groups that should all be merged into one group, use curly braces (brackets) to contain a list of these groups, separated by newlines. The line following the closing bracket should be the name of the group to merge into.

For vertex groups that should be reassigned to a ValveBiped vertex group, use square brackets, and a colon to separate the old group from the new group. For an example, see below:

10
{
thigh1.L
thigh2.L
thigh3.L
}
hip_group
{
forearm1.L
forearm2.L
forearm3.L
}
forearm_group
\[
pelvis:ValveBiped.Bip01_Pelvis
lower_lumbar:ValveBiped.Bip01_Spine
upper_lumbar:ValveBiped.Bip01_Spine1
thoracic:ValveBiped.Bip01_Spine2
hip_group:ValveBiped.Bip01_L_Thigh
forearm_group:ValveBiped.Bip01_L_Forearm
]

Save this as a text file and use the options panel or addon preferences panel to load it.
Note that the groups defined in the merge section can be used in the replace section.

# Video 1
https://www.youtube.com/watch?v=n9lmxpjSv0I
# Video 2 (Explanation Starts at 0:39)
https://youtu.be/Fc-asdOZXZM?list=PL7_W6qzKk7Yi_YImOM00yUi0Cu8iqavCj
