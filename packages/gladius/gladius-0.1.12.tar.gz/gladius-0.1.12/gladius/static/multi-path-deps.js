(function(undefined){
    'use strict';

    // Save a reference to the global object (window in the browser)
    var _root = this;
  
    function dependsOn(pathSpec, url) {
        if (pathSpec === "ignore") {
            return false;
        }
        var dependencyPath = pathSpec.split("/");
        var urlPath = url.split("/");
        for (var i = 0; i < urlPath.length; i++) {
            var dependencyElement = dependencyPath.shift();
            var pathElement = urlPath[i];
            if (dependencyElement !== pathElement && dependencyElement !== "*") {
                return false;
            }
            if (dependencyPath.length === 0 || (dependencyPath.length === 1 && dependencyPath[0] === "")) {
                return true;
            }
        }
        return false;
    }

    function refreshPath(path) {
        var eltsWithDeps = htmx.findAll("[multi-path-deps]");
        for (var i = 0; i < eltsWithDeps.length; i++) {
            var elt = eltsWithDeps[i];
            var attr = elt.getAttribute('multi-path-deps');
            var attrs = JSON.parse(attr);
            
            for (var j = 0; j < attrs.length; j++) {
                var a = attrs[j];

                if (dependsOn(a, path)) {
                    htmx.trigger(elt, "multi-path-deps");
                }
            }
        }      
    }    

    htmx.defineExtension('multi-path-deps', {
        onEvent: function (name, evt) {
            if (name === "htmx:beforeOnLoad") {
                var config = evt.detail.requestConfig;
                // mutating call
                if (config.verb !== "get" && evt.target.getAttribute('multi-path-deps') !== 'ignore') {
                    refreshPath(config.path);
                }
            } 
        }
    });

    /**
     *  ********************
     *  Expose functionality
     *  ********************
     */    

    _root.PathDeps = {
        refresh: function(path) {
            refreshPath(path);
        }
    };
            
}).call(this);