#! /usr/bin/python



import os
import pickle
import datetime
import pprint


cmd = "python -m pip install pytz"
os.popen(cmd).readlines()
import pytz



current_path = os.sep.join(os.getcwd().split(os.sep))
last_git_commit_file = current_path + "/test.txt"

last_commit = ""
lastest_commit = ""

'''
Get last time git commit
'''
pkl_file = open(last_git_commit_file, 'r')
last_commit = pickle.load(pkl_file)

print("Last Time Git Commit:")
pprint.pprint(last_commit)

'''
Get lastest commit:
'''
cmd = "git log"
result = os.popen(cmd).readlines()
print(result)
lastest_commit = result[0].split()[1].strip()

print("Lastest Git Commit:")
pprint.pprint(lastest_commit)

output = open(last_git_commit_file, 'w')
pickle.dump(lastest_commit, output)
output.close()

lastest_commit='4e254945b3c78d0f8ad13f0b3a52af756fe31f99'
last_commit='12feffac2be837b5c39412035f6a1089bd5dad9d'

if lastest_commit != last_commit:
	cmd = "cd %s && git diff %s %s | findstr /b diff" % (current_path, lastest_commit, last_commit)
	print(cmd)
	result = os.popen(cmd).readlines()
	pprint.pprint(result)
	if result:
		for line in result:
			git_diff = line.strip("diff --git ").strip("\n").split()
			what_change = git_diff[0].split("/")
			which_env = what_change[1]
			which_component = what_change[-1].split("-")[0]
			print("git diff: %s" % git_diff)
			print("what_change: %s" % what_change)
			print("which_env: %s" % which_env)
			print("which_component: %s" % which_component)
			
			'''
			Create Stack
			'''
			stack_name = "mystack-%s-" % which_component
			stack_name += datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime("%Y%m%d%H%M%S")
			template_body = "file://%s/%s/templates/%s-template.json" % (current_path, which_env, which_component)
			cmd = "aws --profile %s cloudformation create-stack --stack-name %s --template-body %s" % \
						(which_env, stack_name, template_body)
            
			print("CloudFormation cmd: %s" % cmd)
			result = os.popen(cmd).readlines()
			print("Create Stack: %s, %s" % (which_env, stack_name))
			pprint.pprint(result)
else:
    print("No any change.")



