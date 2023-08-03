<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

	<xsl:template match="/">
		<html>
			<!--- ce chemin est ../HTMLstyle.css car on doit sortir du dossier html_pages, puis chercher le fichier HTMLstyle.css  -->
			<link rel="stylesheet" href="../HTMLstyle.css" />
			<head>
				<title>Facebook profile</title>

			</head>
			<body>
				<h1>Profile of <xsl:value-of select="facebookProfile/username"/>   </h1>
				<table border="1">
					<tr>
						<th>Firstname</th>
						<td>
							<xsl:value-of select="facebookProfile/firstName"/>
						</td>
					</tr>
					<tr>
						<th>Lastname</th>
						<td>
							<xsl:value-of select="facebookProfile/lastName"/>
						</td>
					</tr>
					<tr>
						<th>Username</th>
						<td>
							<xsl:value-of select="facebookProfile/username"/>
						</td>
					</tr>
					<tr>
						<th>Email</th>
						<td>
							<xsl:value-of select="facebookProfile/email"/>
						</td>
					</tr>
					<tr>
						<th>Password</th>
						<td>
							<xsl:value-of select="facebookProfile/password"/>
						</td>
					</tr>
					<tr>
						<th>Date of Birth</th>
						<td>
							<xsl:value-of select="facebookProfile/dateOfBirth"/>
						</td>
					</tr>
					<tr>
						<th>Gender</th>
						<td>
							<xsl:value-of select="facebookProfile/gender"/>
						</td>
					</tr>
					<tr>
						<th>Hometown</th>
						<td>
							<xsl:value-of select="facebookProfile/hometown"/>
						</td>
					</tr>
					<tr>
						<th>Location</th>
						<td>
							<xsl:value-of select="facebookProfile/location"/>
						</td>
					</tr>
					<tr>
						<th>Education</th>
						<td>
							<table border="1">
								<tr>
									<th>School</th>
									<td>
										<xsl:value-of select="facebookProfile/education/school"/>
									</td>
								</tr>
								<tr>
									<th>Degree</th>
									<td>
										<xsl:value-of select="facebookProfile/education/degree"/>
									</td>
								</tr>
								<tr>
									<th>Field of Study</th>
									<td>
										<xsl:value-of select="facebookProfile/education/fieldOfStudy"/>
									</td>
								</tr>
								<tr>
									<th>Graduation Year</th>
									<td>
										<xsl:value-of select="facebookProfile/education/graduationYear"/>
									</td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<th>Work</th>
						<td>
							<table border="1">
								<tr>
									<th>Company</th>
									<td>
										<xsl:value-of select="facebookProfile/work/company"/>
									</td>
								</tr>
								<tr>
									<th>Position</th>
									<td>
										<xsl:value-of select="facebookProfile/work/position"/>
									</td>
								</tr>
								<tr>
									<th>Start Date</th>
									<td>
										<xsl:value-of select="facebookProfile/work/startDate"/>
									</td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<th>About</th>
						<td>
							<xsl:value-of select="facebookProfile/about"/>
						</td>
					</tr>
					<tr>
						<th>Interests</th>
						<td>
							<ul>
								<xsl:for-each select="facebookProfile/interests/interest">
									<li>
										<xsl:value-of select="."/>
									</li>
								</xsl:for-each>
							</ul>
						</td>
					</tr>
					<tr>
						<th>Friends</th>
						<td>
							<table border="1">
								<tr>
									<th>ID</th>
									<th>First Name</th>
									<th>Last Name</th>
									<th>Username</th>
								</tr>
								<xsl:for-each select="facebookProfile/friends/friend">
									<tr>

										<td>
											<xsl:value-of select="@id"/>
										</td>

										<td>
											<xsl:value-of select="firstName"/>
										</td>
										<td>
											<xsl:value-of select="lastName"/>
										</td>
										<td>
											<xsl:value-of select="username"/>
										</td>
									</tr>
								</xsl:for-each>
							</table>
						</td>
					</tr>
				</table>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
