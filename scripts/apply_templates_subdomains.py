import os, re, sys
import glob
import subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape

"""
Apply Default Values to 
SUBDOMAINS Jinja Templates


This script applies default values to 
templates in this folder.

The templates are used by Ansible,
but this script uses the same template
engine as Ansible to apply template
variable values to the template files
and make real files.

only variables are:
    - `username` - user/group name to change ownership to
    - `server_name_default` - name of server 
      (e.g., charlesreid1.com or charlesreid1.red)
"""


# Where templates live
TEMPLATEDIR = '.'

# Where rendered templates will go
OUTDIR = 'output'

# Should existing (destination) files 
# be overwritten if they exist?
OVERWRITE = True

# Template variables
TV = {
        'server_name_default':  'charlesreid1.red',
        'username':             'charles'
}



def apply_templates(template_dir, output_dir, template_vars, overwrite=False):
    """Apply the template variables 
    to the template files.
    """

    if not os.path.exists(output_dir):
        msg = "Error: output dir %s does not exist!"%(output_dir)
        raise Exception(msg)

    if not os.path.exists(template_dir):
        msg = "Error: template dir %s does not exist!"%(output_dir)
        raise Exception(msg)

    # Jinja env
    env = Environment(loader=FileSystemLoader('.'))

    # Render templates
    template_files = glob.glob('*_setup.py.j2') + glob.glob('*_pull.py.j2')
    render_files = [re.sub('\.j2','',s) for s in template_files]

    for rfile,tfile in zip(render_files,template_files):

        # Get rendered template content
        content = env.get_template(tfile).render(**template_vars)

        # Write to file
        dest = os.path.join(output_dir,rfile)
        if os.path.exists(dest) and overwrite is False:
            msg = "Error: template rendering destination %s already exists!"%(dest)
            raise Exception(msg)

        with open(dest,'w') as f:
            f.write(content)

    x = 'executioner.py'
    subprocess.call(['cp',x,os.path.join(output_dir,x)])

    print("Rendered the following templates:%s\nOutput files:%s\n"%(
            "".join(["\n- "+os.path.join(template_dir,j) for j in template_files]),
            "".join(["\n- "+os.path.join(output_dir,j) for j in render_files])
    ))


if __name__=="__main__":
    apply_templates(TEMPLATEDIR,OUTDIR,TV,OVERWRITE)

