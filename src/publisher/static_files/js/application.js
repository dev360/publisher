if (window.location.hash == "#_")
  window.location.hash = "#";


// Provide top-level namespaces for our javascript.
(function() {
  window.publisher = {}

  // Set the class namespaces
  publisher.forms = {};
  publisher.routers = {};
  publisher.models = {};
  publisher.views = {};

  // Set instance namespaces where
  // instances of the classes will live
  publisher.app = {};
  publisher.app.routers = {};
  publisher.app.ui = {};
  publisher.app.data = {}; 




})();

