function collapseSectionsGallery() {
  //we are in edit or add nitf content
  if($("body").hasClass("template-openmultimedia.contenttypes.gallery")  || 
    $("body").hasClass("portaltype-openmultimedia-contenttypes-gallery") && $("body").hasClass("template-edit")) {
      $("fieldset").each(function(index) {
       if(index != 0) {
         $(this).collapse({ closed : true });
       } else {
         $(this).collapse();
       }
     });
   } 
}

$(document).ready(function() {
  collapseSectionsGallery();
});
