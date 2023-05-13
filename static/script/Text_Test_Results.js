fetch('text_results')
  .then(response => response.json())
  .then(data => {
    // Do something with the retrieved data
    // console.log(data);
    var tableContainer = document.getElementById("myTable");

    // Create a table element
    var table = document.createElement("table");

    // Create the table headings row
  var headingsRow = document.createElement("tr");
  var blankHeading = document.createElement("th");
  // headingsRow.appendChild(blankHeading); // add blank cell to top left corner
  for (var i = 0; i < 4; i++) {
    var heading = document.createElement("th");
    if(i==0)
    {
      var headingText = document.createTextNode("Question");
      heading.appendChild(headingText);
      headingsRow.appendChild(heading);
    }
    if(i==1)
    {
      var headingText = document.createTextNode("Prefered Answer");
      heading.appendChild(headingText);
      headingsRow.appendChild(heading);
    }
    if(i==2)
    {
      var headingText = document.createTextNode("Your Answer");
      heading.appendChild(headingText);
      headingsRow.appendChild(heading);
    }
    if(i==3)
    {
      var headingText = document.createTextNode("Similarity");
      // headingText = (headingText * 100).toFixed(2) + '%'
      heading.appendChild(headingText);
      headingsRow.appendChild(heading);
    }
  }
  table.appendChild(headingsRow);

    // Loop through the arrays and create table rows and cells
    for (var i = 0; i < 10; i++) {
      var row = document.createElement("tr");
      for (var j = 0; j < 4; j++) {
        var cell = document.createElement("td");
        var cellText = '';
        if(j==3){
          var similarity = parseFloat(data[i][j]);
          var similarityPercentage = (similarity * 100).toFixed(2) + '%';
          cellText = document.createTextNode(similarityPercentage);
        }
        else
        {
          cellText = document.createTextNode(data[i][j]);
        }
        // console.log(cellText)
        cell.appendChild(cellText);
        row.appendChild(cell);
      }
      // console.log("newrow")
      table.appendChild(row);
    }

    // Append the table to the container div element
    tableContainer.appendChild(table);
  })
  .catch(error => console.error(error));