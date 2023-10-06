from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


########################################
# CONFIGURATION
########################################

CMS_MEMORY_REQUEST_MB = 768
CMS_WORKER_MEMORY_REQUEST_MB = 1024
LMS_MEMORY_REQUEST_MB = 768
LMS_WORKER_MEMORY_REQUEST_MB = 1024

config = {
    # Add here your new settings
    "defaults": {
        "CMS_MEMORY_REQUEST": f"{CMS_MEMORY_REQUEST_MB}Mi",
        "LMS_MEMORY_REQUEST": f"{LMS_MEMORY_REQUEST_MB}Mi",

        # Kubernetes autoscaling settings
        "CMS_AUTOSCALING": True,
        "CMS_AVG_CPU": 75,
        "CMS_AVG_MEMORY": "",
        "CMS_CPU_LIMIT": 2,
        "CMS_CPU_REQUEST": 0.1,
        "CMS_MAX_REPLICAS": 2,
        "CMS_MEMORY_LIMIT": f"{round(CMS_MEMORY_REQUEST_MB * 1.35)}Mi",
        "CMS_MIN_REPLICAS": 1,

        "CMS_WORKER_AUTOSCALING": True,
        "CMS_WORKER_AVG_CPU": 80,
        "CMS_WORKER_AVG_MEMORY": "",  # Disable memory-based autoscaling
        "CMS_WORKER_CPU_LIMIT": 2.5,
        "CMS_WORKER_CPU_REQUEST": 0.1,
        "CMS_WORKER_MAX_REPLICAS": 4,
        "CMS_WORKER_MEMORY_LIMIT": f"{round(CMS_WORKER_MEMORY_REQUEST_MB * 1.35)}Mi",
        "CMS_WORKER_MEMORY_REQUEST": f"{CMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "CMS_WORKER_MIN_REPLICAS": 1,

        "LMS_AUTOSCALING": True,
        "LMS_AVG_CPU": 75,
        "LMS_AVG_MEMORY": "",
        "LMS_CPU_LIMIT": 2,
        "LMS_CPU_REQUEST": 0.1,
        "LMS_MAX_REPLICAS": 2,
        "LMS_MEMORY_LIMIT": f"{round(LMS_MEMORY_REQUEST_MB * 1.35)}Mi",
        "LMS_MIN_REPLICAS": 1,

        "LMS_WORKER_AUTOSCALING": True,
        "LMS_WORKER_AVG_CPU": 80,
        "LMS_WORKER_AVG_MEMORY": "",  # Disable memory-based autoscaling
        "LMS_WORKER_CPU_LIMIT": 2,
        "LMS_WORKER_CPU_REQUEST": 0.1,
        "LMS_WORKER_MAX_REPLICAS": 4,
        "LMS_WORKER_MEMORY_LIMIT": f"{round(LMS_WORKER_MEMORY_REQUEST_MB * 1.35)}Mi",
        "LMS_WORKER_MEMORY_REQUEST": f"{LMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "LMS_WORKER_MIN_REPLICAS": 1,
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {},
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {},
}

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"HPA_{key}", value)
        for key, value in config["defaults"].items()
    ]
)

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'HPA_'.
        ("HPA_VERSION", __version__),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'HPA_'.
        # For example:
        # ("HPA_SECRET_KEY", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        # ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To run the script from templates/hpa/tasks/myservice/init, add:
# hooks.Filters.COMMANDS_INIT.add_item((
#     "myservice",
#     ("hpa", "tasks", "myservice", "init"),
# ))


########################################
# DOCKER IMAGE MANAGEMENT
########################################

# To build an image with `tutor images build myimage`, add a Dockerfile to templates/hpa/build/myimage and write:
# hooks.Filters.IMAGES_BUILD.add_item((
#     "myimage",
#     ("plugins", "hpa", "build", "myimage"),
#     "docker.io/myimage:{{ HPA_VERSION }}",
#     (),
# )

# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:{{ HPA_VERSION }}",
# )
# hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:{{ HPA_VERSION }}",
# )


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorhpa", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("hpa/build", "plugins"),
        ("hpa/apps", "plugins"),
        ("hpa/k8s", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorhpa/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorhpa", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
