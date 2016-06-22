var CongressionalGuide = new Marionette.Application();
CongressionalGuide.addRegions({
    header : 'header',
    main   : '#main',
    footer : 'footer'
});

CongressionalGuide.navigate = function(route,  options){
  options || (options = {});
  Backbone.history.navigate(route, options);
};

CongressionalGuide.on('initialize:after', function(){
    if(Backbone.history){
        Backbone.history.start();

        if(this.getCurrentRoute() === ""){
          ContactManager.trigger("representatives");
        }
    } 
});


$(function(){
    CongressionalGuide.start();
});