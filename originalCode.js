//self invoked function (so it doesn't pollute the global scope)
(async function () {
   // Remove the "Please use the website's Print button to print this page." message.
   document.getElementById("app").classList.remove("By1np"); 
   
   // Disable the @media print {display: none;} on the tab elements.
   const style = document.createElement("style");
   style.textContent = `
      @media print {
         .Cw81bf, .B6413b, .Chcfq, .Cpk34y {
         display: revert !important;
         }
      }
   `;
   document.head.appendChild(style);
   
   // Ensure all lines are loaded by scrolling to them
   const lines = document.getElementById("tablature").children
   undefined
   for (i=0;i<lines.length;i++) {
      lines[i].scrollIntoView();
      await new Promise(r => setTimeout(r, 100));  // Wait a bit so it actually loads
   } 
   
   // Bring up the print dialogue
   print();  
})();
