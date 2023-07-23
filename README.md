# intermediary-tooling
aka what if duvetmc screwed up their intermediaries yet again

## What is this?
This is a version of Fabric's [intermediaries](https://github.com/fabricmc/intermediary), but redone from the ground up
to be across *every version of Minecraft* ever released. Because of the way it's done, these intermediaries are
completely different from Fabric's.

## Why?
Because some of us felt like it. Also, Fabric's intermediaries only go as far back as the 1.14 snapshots, which is lame
and boring. We want to go back to the very beginning.

## How?
Through a combination of a hacky Python script, skyrising's [matches](https://github.com/skyrising/matches)
(for pre-1.14), Fabric's [matches](https://github.com/FabricMC/intermediary/tree/master/matches) (for 1.14+), and way
too much effort, we create a bunch of files to allow intermediaries on every version of Minecraft.

## Submodules...?
This consists of three (technically four) submodules:
- `intermediary`: The place where all the intermediaries end up.
- `matches`: Matches through 1.13.2, provided by skyrising and a bunch of other cool people.
- `mc-versions`: a dependency of `matches`, containing a bunch of metadata that we really don't care about.
- `fabric-intermediaries`: Technically meant for Fabric's intermediary storage, it also contains matches for 1.14+.
