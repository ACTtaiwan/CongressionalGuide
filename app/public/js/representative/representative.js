CongressionalGuide.module("RepresentativeModule", 
    function(RepresentativeModule, CongressionalGuide, Backbone, Marionette, $, _){

    RepresentativeModule.Router = Marionette.AppRouter.extend({
        appRoutes: {
            "representatives": "listRepresentative",
            "representative/:id": "showRepresentative"
        }
    });

});