var barColors = [
    'rgba(35, 39, 42)',
    'rgba(195, 42, 163)',
    'rgba(59, 119, 242)',
    'rgba(189, 8, 28)',
    'rgba(29, 161, 242)',
    'rgba(10, 102, 194)',
    'rgba(201, 203, 207)',
    'rgba(180, 159, 64)',
  ];



// PROFILE STAT CHART
new Chart("profileStats", {
    type: "doughnut",
    
    data: {
      
      labels: category,
      datasets: [{
        backgroundColor: barColors,
        borderColor: [
          'rgba(255, 255, 255, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1,
        data: category_visit,
        hoverBorderWidth:8
      }]
    },
    options: {
      title: {
        display: true,
        text: "Links Visitors"
      },
      legend:{
        display: true,
      },
      scales:{

 
      }
  
    }
  });

  new Chart("profileVisits", {
    type: "line",
    
    data: {
      
      labels: day,
      datasets: [{
        backgroundColor: 'rgba(154, 80, 235, 1)',
        borderColor: [

          'rgba(0, 0, 0, 1)',
 
      ],
      borderWidth: 4,
        data: day_visit,
        hoverBorderWidth:8
      }]
    },
    options: {
      title: {
        display: true,
        text: "Profile Visitors"
      },
      legend:{
        display: false,
      },
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero: true
          }
        }]

 
      }
  
    }
  });
