function getHiddenProp(){
    var prefixes = ['webkit','moz','ms','o'];
    
    // if 'hidden' is natively supported just return it
    if ('hidden' in document) return 'hidden';
    
    // otherwise loop over all the known prefixes until we find one
    for (var i = 0; i < prefixes.length; i++){
        if ((prefixes[i] + 'Hidden') in document) 
            return prefixes[i] + 'Hidden';
    }

    // otherwise it's not supported
    return null;
}

function isHidden() {
    var prop = getHiddenProp();
    if (!prop) return false;
    
    return document[prop];
}

window.addEventListener("load", function simpleDemo() {
  // use the property name to generate the prefixed event name
  autoRefresh();
  var visProp = getHiddenProp();
  if (visProp) {
    var evtname = visProp.replace(/[H|h]idden/,'') + 'visibilitychange';
    document.addEventListener(evtname, autoRefresh);
  }
  else {
      var txtFld = document.getElementById('enableAutoRefresh');
      txtFld.value += "PageVisibilityAPI not supported!"
  }

  function autoRefresh() {
    var txtFld = document.getElementById('enableAutoRefresh');
    if (txtFld) {
      if (isHidden()) {
        //page is hidden

      }
      else {
        //page is visible, autorefresh page every 15 seconds
        setTimeout("location.reload(true);",15000);
      }
    }
  }
});