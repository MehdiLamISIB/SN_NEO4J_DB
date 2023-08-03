import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from lxml import etree
from datetime import datetime
from py2neo import Graph
import csv

# user: neo4j
# mdp : isibmehdi
# Connect to Neo4j


### Utilisation de la librairie py2neo pour acceder à la base donnée neo4j
graph = Graph(host="localhost",name="facebook", auth=("neo4j", "isibmehdi"))
### Je lance une requête pour récuperer tout les éléments de la base données (Noeuds & Relations)
profiles= graph.run("Match(p:Profile) return p")
profiles=profiles.data()
def Neo4j_to_XML():
    for p in profiles:
        """
        -----------------------------
        -----------------------------
        Recuperation des données neo4j
        -----------------------------
        -----------------------------
        """
        node=p["p"]
        work="match(p:Profile)-[:WORKTO]->(w:Work) where p.id=\"{0}\" return w".format(node["id"])
        education="match(p:Profile)-[:EDUCATEDTO]->(e:Education) where p.id=\"{0}\" return e".format(node["id"])
        interests="match(p:Profile)-[:HASINTEREST]->(ints:Interests) where p.id=\"{0}\" return ints".format(node["id"])
        friends="match(p:Profile)-[:ISFRIENDWITH]->(f:Profile) where p.id=\"{0}\" return f.id,f.firstName,f.lastName,f.username".format(node["id"])
        work=graph.run(work).data()
        work=work[0]["w"]
        education=graph.run(education).data()
        education=education[0]["e"]
        interests=graph.run(interests).data()
        interests=interests[0]["ints"]["interest"]
        friends=graph.run(friends).data()
        ### creer fichier xml
        xml_file= create_XML_fromNeo4j(node,work,education,interests,friends)
        dom = minidom.parseString(xml_file)
        pretty_xml = dom.toprettyxml()
        path_file="xml_DATA/profile_id_{0}.xml".format(node["id"])
        f = open(path_file, "wb")
        f.write(pretty_xml.encode('utf-8'))
        f.close()
        ### VALIDATION XSD
        if(validate_xml(path_file)):
            print("le fichier xml du profile {0} a été validé".format(node["id"]))
        else:
            print("le fichier xml du profile {0} n'as pas été validé".format(node["id"]))
            return False
    return True
def create_XML_fromNeo4j(node,work,education,interests,friends):
    """
    -----------------------------
    transfert avec xml !!!!
    -----------------------------
    Je crée les différents element xml pour le profil à partir d'un noeud Neo4j Profile
    """
    root=ET.Element("facebookProfile")
    root.set("id",node["id"])
    profile = root
    ET.SubElement(profile, "firstName").text = node["firstName"]
    ET.SubElement(profile, "lastName").text = node["lastName"]
    ET.SubElement(profile, "username").text = node["username"]
    ET.SubElement(profile, "email").text = node["email"]
    ET.SubElement(profile, "password").text = node["password"]
    #FORMATAGE TEXT DATE
    dateOfBirth= datetime.strptime(node["dateOfBirth"], '%m/%d/%Y')  #.strftime("%Y-%m-%d")
    dateOfBirth=dateOfBirth.strftime("%Y-%m-%d")
    #print(dateOfBirth)
    ET.SubElement(profile, "dateOfBirth").text = dateOfBirth #node["dateOfBirth"]
    ET.SubElement(profile, "gender").text = node["gender"]
    ET.SubElement(profile, "hometown").text = node["hometown"]
    ET.SubElement(profile, "location").text = node["location"]
    #### EDUCATION
    ET_education=ET.SubElement(profile,"education")
    ET.SubElement(ET_education,"school").text=education["school"]
    ET.SubElement(ET_education, "degree").text = education["degree"]
    ET.SubElement(ET_education, "fieldOfStudy").text = education["fieldOfStudy"]
    ET.SubElement(ET_education, "graduationYear").text = education["graduationYear"]
    #### WORK
    ET_work=ET.SubElement(profile,"work")
    ET.SubElement(ET_work,"company").text=work["company"]
    ET.SubElement(ET_work,"position").text= work["position"]
    #Formatage de texte pour la date
    startDate= datetime.strptime(work["startDate"], '%m/%d/%Y')  #.strftime("%Y-%m-%d")
    startDate=startDate.strftime("%Y-%m-%d")
    #print(startDate)
    ET.SubElement(ET_work,"startDate").text= startDate #work["startDate"]
    #### ABOUT
    ET.SubElement(profile, "about").text = str(node["about"])
    #### INTERESTS
    ET_interests=ET.SubElement(profile,"interests")
    for ints in interests:
        ET.SubElement(ET_interests, "interest").text = ints
    #### FRIENDS
    ET_friends=ET.SubElement(profile,"friends")
    for f in friends:
        ET_friend=ET.SubElement(ET_friends,"friend")
        ET_friend.set("id",f["f.id"])
        ET.SubElement(ET_friend,"firstName").text= f["f.firstName"]
        ET.SubElement(ET_friend, "lastName").text= f["f.lastName"]
        ET.SubElement(ET_friend, "username").text= f["f.username"]
    xml_str = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return xml_str
    #print(xml_str.decode("utf-8"))
def validate_xml(xml_path):
    """
        Cette méthode permet de vérifier et valider le fichier xml avec le xsd correspondant
    :param xml_path: le chemin d'accès du fichier xml à valider
    :return:
    """
    xsd_file=etree.parse("schemaFinal.xsd")
    xsd_file=etree.XMLSchema(xsd_file)
    result=xsd_file.validate(etree.parse(xml_path))
    return result
def xmltocsv():
    """
        Pour transformer les données en csv, je choisis les tags qui seront utilisés pour les colonnes
        Le format choisi pour gérer plusieurs éléments dans une même colonne est le ';' (par exemple la colonne Friends et Interests)
        Je vais donc créér une ligne pour le profil et l'écrire dans un fichier texte qui sera FacebookProfile.csv
    """
    with open('facebookProfile.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id_profile','firstName', 'lastName','username', 'email','password', 'dateOfBirth', 'gender',
                         'hometown', 'location',
                         'school', 'degree', 'fieldOfStudy',
                         'company', 'position', 'startDate','about',
                         'interests',
                         'id_friend','friend_firstName','friend_lastName','friend_username'])
        row=[]
        """
            Une ligne représente un profil, je vais donc récuprer le fichier xml correspodant avec son profil_id _{id}.xml
        """
        for p in profiles:
            node = p["p"]
            path_file = "xml_DATA/profile_id_{0}.xml".format(node["id"])
            tree = ET.parse(path_file)
            root = tree.getroot()
            ######
            interests=[]
            for hobby in root.findall('.//interests/interest'):
                interests.append(hobby.text)
            friend_id=[]
            friend_fn=[]
            friend_ln=[]
            friend_un=[]
            for friend in root.findall('.//friends/friend'):
                friend_id.append(friend.get('id'))
                friend_fn.append(friend.find('firstName').text)
                friend_ln.append(friend.find('lastName').text)
                friend_un.append(friend.find('username').text)
            ### creation de la ligne de donnée
            row = [
                root.get('id'),
                root.find('firstName').text,
                root.find('lastName').text,
                root.find('username').text,
                root.find('email').text,
                root.find('password').text,
                root.find('dateOfBirth').text,
                root.find('gender').text,
                root.find('hometown').text,
                root.find('location').text,
                root.find('.//education/school').text,
                root.find('.//education/degree').text,
                root.find('.//education/fieldOfStudy').text,
                root.find('.//work/company').text,
                root.find('.//work/position').text,
                root.find('.//work/startDate').text,
                root.find('about').text,
                ';'.join(interests),
                ';'.join(friend_id),
                ';'.join(friend_fn),
                ';'.join(friend_ln),
                ';'.join(friend_un)
            ]
            #print(row)
            writer.writerow(row)

def xmlToXSLT():
    """
        Va parcourir chaque profil et créer un fichier html en utilisant un xslt pour la structure
    """
    for p in profiles:
        node = p["p"]
        path_file = "xml_DATA/profile_id_{0}.xml".format(node["id"])
        xml_doc = etree.parse(path_file)
        xslt_doc = etree.parse("facebook.xslt")
        transformer = etree.XSLT(xslt_doc)

        html_page = transformer(xml_doc)

        with open("html_pages/facebookPage_id_{0}.html".format(node["id"]), "wb") as file:
            file.write(html_page)

if( Neo4j_to_XML() ):
    print("Je peux transferer toute les données vers le CSV")
    xmltocsv()
    xmlToXSLT()
    print()
    print("Tout les profils ont un xml et une page html associés !!!!")
else:
    print("Je ne peux pas transferer toute les données vers le CSV")

# permet de tout supprimer :
# MATCH (n)
# DETACH DELETE n

