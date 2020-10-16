from .ReportDaily import *

# Lists the total number of repositories
class ReportRepositoryHistory(ReportDaily):
	def name(self):
		return "repository-history"

	def updateDailyData(self):
		self.header, newData = self.parseData(self.executeQuery(self.query()))
		self.data.extend(newData)
		self.truncateData(self.timeRangeTotal())
		self.sortDataByDate()

	# Collects the number of repositories for a user type (user/organization) given a time range
	def queryRepos(self, userType):
		query = '''
			SELECT
				COUNT(*) AS count
			FROM
				repositories
				JOIN users ON repositories.owner_id = users.id
			WHERE
				TRUE
				''' + self.andExcludedEntities("users.login") + '''
				''' + self.andExcludedEntities("repositories.name")

		if userType != None:
			query += '''
				AND users.type = "''' + userType + '''"'''

		return query

	# Collects the number of forks for a user type (user/organization) given a time range
	def queryForks(self, userType):
		query = '''
			SELECT
				COUNT(*) AS count
			FROM
				repositories
				JOIN users ON repositories.owner_id = users.id
			WHERE
				repositories.parent_id IS NOT NULL
				''' + self.andExcludedEntities("users.login") + '''
				''' + self.andExcludedEntities("repositories.name")

		if userType != None:
			query += '''
				AND users.type = "''' + userType + '''"'''

		return query

	# Collects the number of repositories and forks in total, in organizations, and in user accounts
	def query(self):
		return '''
			SELECT
				"''' + str(self.yesterday()) + '''" AS date,
				total.count AS total,
				organizationSpace.count AS "repos in organizations",
				userSpace.count AS "repos in user accounts",
				totalForks.count AS "forks total",
				organizationSpaceForks.count AS "forks in organizations",
				userSpaceForks.count AS "forks in user accounts"
			FROM
				(''' + self.queryRepos(None) + ''') AS total,
				(''' + self.queryRepos("Organization") + ''') AS organizationSpace,
				(''' + self.queryRepos("User") + ''') AS userSpace,
				(''' + self.queryForks(None) + ''') AS totalForks,
				(''' + self.queryForks("Organization") + ''') AS organizationSpaceForks,
				(''' + self.queryForks("User") + ''') AS userSpaceForks'''
