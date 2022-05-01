//returns a surveyjs page component which contains a bootstrap themed card
    var WelcomePage = (surveyName) =>{
        return( 
      {
        "name": "page1",
        "title": {surveyName},
        "elements": [
            {
                "type": "panel",
                "title": "",
                "elements": [
                    {
                        "type": "html",
                        "name": "testHtml",
                        "html": `
                        <div class="px-4 py-5 my-5 text-center">
                        <!--<img class="d-block mx-auto mb-4" src="/survey/public/logo_snet_long.png" alt="snet logo large" width="72" height="57"-->
                        <h1 class="display-5 fw-bold">${surveyName}</h1>
                        <div class="col-lg-6 mx-auto">
                          <p class="lead mb-4">Welcome to ${surveyName}. Please click next to continue.</p>
                        </div>
                      </div>
                      `
                    }
                ]
            }
        ]

    })
}

export default  WelcomePage