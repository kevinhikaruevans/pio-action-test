import subprocess
import re
import array

Import("env")

print("Current CLI targets", COMMAND_LINE_TARGETS)
print("Current Build targets", BUILD_TARGETS)

HEADER_SIZE = 64

def get_git_repo_name() -> bytes:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"], 
            stdout=subprocess.PIPE, 
            text=True, 
            check=True
        )
        match = re.search(r'([^/]+)\.git$', result.stdout.strip())
        return match.group(1).encode()
        
    except:
        return b'unknown'
    
def post_program_action(source, target, env):
    program_path: str = source[0].get_abspath()
    repo_name = get_git_repo_name()

    assert len(repo_name) < HEADER_SIZE, 'repo name exceeds header size'
    
    if not program_path.endswith(".bin"):
        print('<- program path does not end in bin - ignoring')
        return
    
    header = bytearray(b'\x00' * HEADER_SIZE)
    header[:len(repo_name)] = repo_name

    with open(program_path, 'rb') as orig_binary:
        with open(f"release.bin", 'wb') as new_binary:
            new_binary.write(header)
            new_binary.write(orig_binary.read())
    

env.AddPostAction("buildprog", post_program_action)


# #
# # Upload actions
# #

# def before_upload(source, target, env):
#     print("before_upload")
#     # do some actions

#     # call Node.JS or other script
#     env.Execute("node --version")


# def after_upload(source, target, env):
#     print("after_upload")
#     # do some actions

# env.AddPreAction("upload", before_upload)
# env.AddPostAction("upload", after_upload)

# #
# # Custom actions when building program/firmware
# #

# env.AddPreAction("buildprog", callback...)
# env.AddPostAction("buildprog", callback...)

# #
# # Custom actions for specific files/objects
# #

# env.AddPreAction("$PROGPATH", callback...)
# env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", [callback1, callback2,...])
# env.AddPostAction("$BUILD_DIR/${PROGNAME}.hex", callback...)

# # custom action before building SPIFFS image. For example, compress HTML, etc.
# env.AddPreAction("$BUILD_DIR/spiffs.bin", callback...)

# # custom action for project's main.cpp
# env.AddPostAction("$BUILD_DIR/src/main.cpp.o", callback...)

# # Custom HEX from ELF
# env.AddPostAction(
#     "$BUILD_DIR/${PROGNAME}.elf",
#     env.VerboseAction(" ".join([
#         "$OBJCOPY", "-O", "ihex", "-R", ".eeprom",
#         "$BUILD_DIR/${PROGNAME}.elf", "$BUILD_DIR/${PROGNAME}.hex"
#     ]), "Building $BUILD_DIR/${PROGNAME}.hex")
# )