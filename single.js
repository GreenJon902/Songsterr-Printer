(async function () {
    // If global flag ranByMulti is set then print dialogue won't be opened

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
   const lines = document.getElementById("tablature").children;
   for (i=0;i<lines.length;i++) {
      lines[i].scrollIntoView();
      await new Promise(r => setTimeout(r, 100));  // Wait a bit so it actually loads
   } 
   
   // Bring up the print dialogue
   if (typeof ranByMulti === "undefined") print();  
})();
