import * as Survey from "survey-react"
// create a Survey.PageModel object in surveyjs page format with raw data from backend
function CreateNewQuestion(rawData, itemnr, totalitems){
    var movie_info = "<div class='description_text'><h2>"+ rawData.description.title+"</h2>"+
    "<h4>Year: " + rawData.description.year +
    "<h4>Director: " + rawData.description.director + "</h3>" +
    "<h4>Actors: " + rawData.description.actors + "</h3>" +
    "<p Plot: >" + rawData.description.plot + "</p></div>"

   var progressBar = `
    	<div class= "progress-text">
            <h6>Item ${itemnr} of ${totalitems}</h6>
        </div>
    `
        var newPage = {
            "name": "page",
            "elements": [
                {
                    "type": "html",
                    "name": "info",
                    "html": progressBar
                },
                {
                    "type": "panel",
                    "innerIndent": 1,
                    "name": "panel5",
                // "state": "expanded",
                    "elements": [
                        // poster of the given movie
                        {
                            "type": "image",
                            "name": "banner",
                            "imageLink": rawData.description.poster,
                            "imageWidth": "300px",
                            "imageHeight": "400px",
                        },

                        // description of the given movie
                        {
                            "type": "html",
                            "name": "info",
                            "html": movie_info
                        }
                    ]
                },
                // custom ratings widget
                {
                    "type": "customrating",
                    "name": "" + rawData.item_id,
                    "title": "Please rate the given movie on a scale of 5",
                    "isRequired": true,
                    "value": 2
                }

            ]
        }
    //console.log("newpage")
   // console.log(newPage)
    var page = new Survey.PageModel("newPage")
    page.fromJSON(newPage)
    return page
}

function CreateTemplatePage(itemnr, totalitems){
    var progressBar = `
    	<div class= "progress-text">
            <h6>Item ${itemnr} of ${totalitems}</h6>
        </div>
    `
        var newPage = {
            "name": "page",
            "elements": [
                {
                    "type": "html",
                    "name": "info",
                    "html": progressBar
                }
                

            ]
        }
    //console.log("newpage")
   // console.log(newPage)
    var page = new Survey.PageModel("newPage")
    page.fromJSON(newPage)
    return page
}



function CreateNewPanel(rawData){
    var movie_info = "<div class='description_text'><h2>"+ rawData.next_item.description.title+"</h2>"+
    "<h4>Year: " + rawData.next_item.description.year +
    "<h4>Director: " + rawData.next_item.description.director + "</h3>" +
    "<h4>Actors: " + rawData.next_item.description.actors + "</h3>" +
    "<p Plot: >" + rawData.next_item.description.plot + "</p></div>"


        var newPanel = {

                    "type": "panel",
                    "innerIndent": 1,
                    "name": rawData.next_item.item_id,
                // "state": "expanded",
                   
                    "elements": [
                        // poster of the given movie

                        {
                            "type": "image",
                            "name": "banner",
                            "imageLink": rawData.next_item.description.poster,
                         //   "imageWidth": "300px",
                          //  "imageHeight": "400px",
                        },

                        // description of the given movie
                        {
                            "type": "html",
                            "name": "info",
                            "html": movie_info
                        },
                        {
                            "type": "customrating",
                           // "visibleIf":"{rating} empty",
                            "name": rawData.next_item.item_id,
                            "title": "Please rate the given movie on a scale of 5",
                            "isRequired": true,
                            "value":"rating"
                           
                        },
                        {
                            "type": "text",
                            "visibleIf":"{rating} <-10",
                            "name": "rating", //+ rawData.next_item.item_id,
                            "placeHolder": rawData.next_item.item_id,
                            "isRequired": true,
                            
                        }
                    ]
                }
                // custom ratings widget
        
    //console.log("newpage")
   // console.log(newPage)
    var panel = new Survey.PanelModel('newpanel')
    panel.fromJSON(newPanel)
    return panel
}



export {CreateNewQuestion, CreateTemplatePage, CreateNewPanel}
