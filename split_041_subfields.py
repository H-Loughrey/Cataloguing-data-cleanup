import pymarc as py
import re
from pymarc import MARCReader, Record, Field
from pymarc import MARCWriter
#Written by: Hazel Loughrey (NLNZ)
#Last updated: 17/8/23
#=========================================INFO======================================================================
#Iterates over each 041 field in each record. Then iterates over the characters in 041 fields. When it finds a subfield, it sets
#that as the current subfield. It then splits every 3 characters with the subfield until it finds another one.
#e.g. it looks at a field: '041 ## $a engmao $h fre'
#It looks at the first 3 characters ('$a '), sees it isn't 3 letters and sets that as the sub field. Then finds 'eng', which now goes in $a. etc.
#This is reusable - just change the file name.
#===================================================================================================================

fileName = 'merged_041_set'
field = Field(tag = '041', indicators = [' ', ' '])

with open (fileName + '.mrc', 'rb') as file:
	fileData = MARCReader(file, to_unicode=True, force_utf8=True,)

	#iterate over records
	for record in fileData:
		#get fields, store in variable, delete fields
		all_lang_fields = record.get_fields('041')
		record.remove_fields('041')

		#iterate over 041 fields
		for i in all_lang_fields:
			lang_field = str(i)
			x = 0
			sub = ""

			new_041 = Field(tag = '041', indicators = i.indicators)
			#add placeholder field
			record.add_ordered_field(new_041)

			#iterate over characters in each field
			while x < len(lang_field):
				#if first three letters are letters then
				if 	re.search(r"[a-z]{3}", lang_field[x:x+3]):
					try:
						if sub != "":
							#add subfield, go to next 3 characters.
							new_041.add_subfield(sub, lang_field[x:x+3])
							x += 3
					except:
						print("couldn't add subfield '" + sub + " " + lang_field[x:x+3] + "' from " + lang_field)
						x += 3

				#else skip past the subfield tag, and set it as new subfield
				elif re.search(r"\$\w", str(lang_field[x:x+2])):
					sub = lang_field[x+1:x+2]
					x += 2
				else:
					#otherwise skip a charcter and try again
					x += 1

		writer = MARCWriter(open(fileName + '_UPDATED.mrc','ab'))
		writer.write(record)
		writer.close()