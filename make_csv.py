'''
make_csv.py
Make a master csv file containing table of pertinent repo info
New columns include individual months from start to end of entire time frame
	Row values are # commits in the individual months
Plan to analyze csv file in R
Input:  pickle file based on json file (built from get_stats.py)
'''
import sys, json, pickle

def timestamp_to_nth_month(commit_time,first_commit_time):
	'''
		Return the nth month in the time interval of commits
		Helper function to process list of commits
	'''
	diff_years = int(commit_time[:4])-int(first_commit_time[:4])-1
	diff_months = int(commit_time[5:7])+(12-int(first_commit_time[5:7]))
	diff_months = diff_years*12+diff_months
	return diff_months

def get_commit_months(commit_list):
	'''
		Commit list has timestamps. 
		Convert timestamps to nth month in repo life
	'''
	# Slice for year-month-day from timestamp
	commit_list = [c[:10] for c in commit_list]
	first_commit_time = commit_list[-1]
	last_commit_time = commit_list[0]
	
	# Get total months from first to last commit
	years = int(last_commit_time[:4])-int(first_commit_time[:4])-1
	months = int(last_commit_time[5:7])+(12-int(first_commit_time[5:7]))
	months = years*12+months

	commit_time = commit_list[4]
	# print(timestamp_to_nth_month(commit_time,first_commit_time))

	# print("\n")
	commit_list = [timestamp_to_nth_month(commit,first_commit_time) for commit in commit_list]
	# print(commit_list)
	montly_commits = [ (i,commit_list.count(i)) for i in set(commit_list) ]
	return montly_commits


def write_csv(file_string):
	'''
		Write csv with relevant info from json
	'''
	output = open(file_string+".all_info.csv","w")
	START_YR = 1996
	END_YR = 2017
	print("Loading pickle...")
	data = open(file_string,"rb")
	data = pickle.load(data)
	print("Writing entries...")
	for repo in data:
		commit_months = get_commit_months(repo["commits"])
		output.write(repo["full_name"]+" "+str(commit_months)+"\n")
file_string = sys.argv[1]
write_csv(file_string)
