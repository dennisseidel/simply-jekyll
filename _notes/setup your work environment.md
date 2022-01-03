---
tags: type/howto operationalexcellence
season: winter
classification: public
title: 'how to setup obsidianmd with para, note taking & tasks'
aliases: []
---

This article describes how you setup your work environment to be productive. I'm a knowledge worker so, at the core at what I do is writing. Therefore, this setup focuses on my writing environment. It use [Obsidian](https://obsidian.md/) to organize what I you do and write. The high-level structure are PARA folders.[^1] You'll create and configure folder, plugin, and template to setup the *general organization & usability*, the *task management & note taking* and finally the folders for *projects*, *areas*, and *resources*. The setup avoids plugins & fancy features. If you have ideas to simplify the setup [mail me](mailto://ds@dennisseidel.de)  I'm always happy to improve 😊  

### Organization & Usability

1.  Plugin Folder Notes:[^6] I use folder notes so I can organize projects and areas in folders and have one entrypoint to the folders.   
2.  Plugin Dataview:[^7] I query in the daily note the open task to get a overview.
3. Folder  `templates`: I create template folder.

I suggest you add some convenience plugins: 

- [Cycle through planes](https://github.com/phibr0/cycle-through-panes): Helps you to tab though multiple planes
- [Collapse all](https://github.com/OfficerHalf/obsidian-collapse-all): Collapses all folders in your sidebar.
- [Footnote shortcut](https://github.com/akaalias/obsidian-footnotes): Footnotes help keep the flow of your notes clean. With the shortcut you can create a footnote in one step. 


### Task Management & Note Taking 

I use simple to-do checkboxes within projects and other files[^10]. To add due dates I use a text expander snippet to add the *task is due on* syntax of the dataview plugin ( `🗓@` ) to tasks. The `@` automatically triggers the [natural dates plugin](https://github.com/argenos/nldates-obsidian). Then I use dataview to query an overview of the tasks. Each evening I look at [[tasks-overview]] & [[task-due]] and add timeboxes for the next day to the calendar. To plan[^16] the I add information about the *situation, notes, and tasks* to the timebox calendar entry .[^11]  The next morning  just typing `;agenda` into my daily note. This snippet creates the day's agenda from my calendar with a script.   

1. Create the [[tasks-overview]], and [[task-due]] **templates** in the `templates` folder: I use the note to show me all open tasks. I use the overview to plan my next day. 
2. Create a the `journals` **folder** for the daily notes.
3. Configure the [periodic notes](https://github.com/liamcain/obsidian-periodic-notes) **plugin** to create a new notes each day where I outline my agenda and note. I use [[day_template]] **template** for each day with sections for the agenda, notes and a link to the task overview query[^3]. 
4. I use the [calendar-to-agenda.py](file:///Users/dennisseidel/OneDrive/backupx/typinator/Sets/Includes/Scripts/calendar-to-agenda.py) script to transform my calendar into my agenda.[^5] 


### Projects

I create for *each of my project* a **folder with a folder note**.[^4]  Then I initialize the project with my project template. The *project template* includes a **checklist with tasks** (with some standard tasks depending on the project type), a **section for done tasks** and a **section for resources**. After I initialized the project, I write down the open tasks. Later after I've finished the tasks, I document them in the *archived section*. The goal is to read the *archived section* and understand what happened. 

1. Create the `01_PPROJECTS` folder and a folder note that holds a list of projects and a list of someday projects (they might be just some text). For each project write down *the KPI and the release schedule* and the DRI[^14].
3.  Create a template: project[^5]
	```markdown
	---
	tags: type/project
	---

	The minimal viable outcome (KPI) of this project is ...

	- [ ] #DRI/DS executed along ....


	## what happened
	- 


	## Footnotes & Resources


	```
1. For each project create a folder with a folder node based on the project template

For each (planned) result in a project only write the achievement and the DRI (with `#` and DRI/Name). Write the details in an article linked in the one-line description. This then also allows us to use the Kanban plugin if we want. The articles also link to the resources. 

Optional: If you have project that require writing complex document, I suggest you use the Longform plugin to better write and edit your text.


### Areas

I create for *each (private) area where I maintain a standard* a **folder including a folder note** inside `02_AREAS`. I initialize the folder note with my **area template**. The area template contains **goal (key results)** and regular habits that help to maintain the standard. These habits lead to timebound projects with clear goals in a certain (short timespan). Finally, I *collect valuable information* in the **resources & footnotes section**.    

1. create folder: `02_AREAS`. 
1.  Create area template[^5]
	```
	---
	tags: type/area
	---
	
	## Key Results
	
	- 
	
	## Habits
	
	- 
	
	## Resources & Footnotes
	```
2. Then I create a overview file in the [[02_AREAS]] folder note. The overview file use `![[investor#Habits]]` syntax to create an overview of all habits and key results of each area. 

I use the overview to regularly check for projects & task I need to start. Further I confirm that I do my habits.


### Resources

I organize (public) "topic or theme of ongoing interest" in the `03_RESOURCE` folder. One folder is a *collection* of related information around this topic. Inside a collection I create articles. Articles are either *whatis* or *howto*.[^15] For more info around the differences check [[knowledge management]]. I name the *whatis* article same as the content the article describes e.g. *artificial intelligence* / *regex*. I name *howto* articles with an howto in the name e.g. *howto implement an artificial intelligence product* / *howto regex*.[^8] I click on the collection folder and then use *Shift - N* to create a new note. whatis articles explain a topic and create understanding / foundations e.g. "what is artificial intelligence". Howto articles describe how to do somethings e.g. "How to implement a model (to identify cars)".    

1. Create `03_RESOURCES` folder with a collection. 
1. Create a collection template

```
---
tags: type/collection
classification: private
title: ''
aliases: []
season: spring
---

This file list all the different articles.

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Title", type AS "Type", tags AS "Tags" FROM #computerscience
WHERE "type != collection" AND contains(tags, "")
SORT file.mtime DESC
/```
```
1. Create articles template

```
---
type: howto|whatis, samplecollectionName, sampleRelatedCollection
season: winter
classification: private
title: ''
aliases: []
---

- Intro (Goal, Situation/Complication/Background) - This article describes ...

- Content (depending on the topics differnt formats e.g. RFC/ADR format, 6 pager ... with differnt chapters)


## Footnotes & Resources



```

1. Use the templates to create the collections and articles. Differentiate between `howto` and `whatis` in the tags and add `relatedCollectionNames`.[^12] 

Optional: You can setup [[devonthink]] for a better search. You also want to prevent to write private information into a public note. The highlight public notes plugin flags public notes based on the frontmatter classification with a read heading.

Optional: You can use the [Obsidian_to_Anki plugin](https://github.com/Pseudonium/Obsidian_to_Anki) to create card. Either by defining the cards (`;ll`) e.g. 
```
START
Cloze
**Halte dich immer an meine {1|Lessons learned}, egal ob es jemand anderem passt oder nicht - es geht um mein {1|Leben und was das Beste ist}.** 
{1| 
}
<!--ID: 1640611254848-->
END

---
```

Or by using inline a custom regex `((?:.+\n)*(?:.*==.*)(?:\n(?:^.{1,3}$|^.{4}(?<!<!--).*))*)` to identify ==highlights== in texts and create clozes from that.  
<!--ID: 1640611254854-->


## Footnotes & Resources

Further I use some non-essential plugins [^13].

- [ ] Merge / link [[productivity setup and process]] and [[knowledge management]] specifically [[howto structure information and articles]] - e.g. like tag management.

---

[^1]: The obisdian forum explains [PARA in the context of Obsidian](https://forum.obsidian.md/t/the-para-method-and-the-hard-facts-of-life/22279) and provides a [starter kit](https://forum.obsidian.md/t/para-starter-kit/223).
[^3]: Idea: Only link to a note that includes the query. that makes it easier for me to work with the daily note. In that note I can then also have multiple queries available. 
[^4]: project should have a clear outcome and you should finish project within a sprint (max a quarter)
[^5]: I execute my scripts with Typinator. e.g. `;agenda`. The template holds a tag with the typ to find archive project later in the archive. 
[^6]: Install the [folder-note](https://github.com/aidenlx/alx-folder-note) and [folder note core](https://github.com/aidenlx/folder-note-core) plugin.
[^7]: Install the [dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin.
[^8]: I use folders for projects an tags for resources [coparision graph](x-devonthink-item://CBCB7FF7-F31A-4265-B0A3-C38A59E7A91F) / [best pratices for finder tags](x-devonthink-item://A15ECE9C-B8D5-4DEA-B2D4-163056D378D2). I tried to simplify by using [index notes](https://github.com/akosbalasko/zoottelkeeper-obsidian-plugin) over tags but the plugin wasn't mature enough. Based on an article why [folders are still the more mature solution](x-devonthink-item://094EAE35-A7CC-4CE6-931E-B9D59D783796)
[^9]: https://osxdaily.com/2012/07/19/hide-file-mac-os-x-chflags/
[^10]: (e.g. areas or daily notes for tasks that just come up and don't belong to a specific project or resource or area, the dataview plugin also allows to plan tasks for a specific due date in the future)
[^11]: It is important to know what the goal is in meetings and share an agenda up front.
[^12]: Alternative: make the route folder of an resource the `whatis` note that explains the resource collection. Then create other sub notes in the right collection and explain the root note what this is. So that you can read the `whatis` note and understand the rough overview of what is in the collection. The tag the article with the `#collectionName` and other related collections. 
[^13]: [incremental writing](https://github.com/bjsi/incremental-writing), Obsidian_to_Anki, ...
[^14]: Based on the [yc guide](https://youtu.be/kzVvjKLdAbk?t=94), *the KPI and the release schedule*. The schedule might be weekly. The DRI is the "head of product".  
[^15]: The [[stackoverflow articles]] concept use also classifies articles into `whatis` and `howto`. 
[^16]: Planning is essential to effiently execute. In my experience if i haven't planned the task of a day, I either plan to much or do them inefffiently.  
