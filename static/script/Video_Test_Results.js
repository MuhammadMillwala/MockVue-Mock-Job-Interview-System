fetch('video_results')
  .then(response => response.json())
  .then(data => {
    // Do something with the retrieved data
    console.log(data);
    var ctx = document.getElementById("myChart").getContext("2d");
    // var data2 = [10, 20, 30, 40, 50, 60, 70, 80];
    var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['angry', 'dusgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'no_face'],
        datasets: [{
          data: data[1],
          backgroundColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(145, 195, 219, 1)',
            'rgba(180, 221, 220, 1)'
          ],
          hoverOffset: 4
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Pie Chart',
          responsive: true,
          maintainAspectRatio: false,
        }
      }
    });

    // Get the container div element
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
    for (var i = 0; i < data[0].length; i++) {
      var row = document.createElement("tr");
      for (var j = 0; j < data[0][i].length; j++) {
        var cell = document.createElement("td");
        var cellText = '';
        if(j==3){
          var similarity = parseFloat(data[0][i][j]);
          var similarityPercentage = (similarity * 100).toFixed(2) + '%';
          cellText = document.createTextNode(similarityPercentage);
        }
        else
        {
          cellText = document.createTextNode(data[0][i][j]);
        }
        cell.appendChild(cellText);
        row.appendChild(cell);
      }
      table.appendChild(row);
    }

    // Append the table to the container div element
    tableContainer.appendChild(table);
  })
  .catch(error => console.error(error));