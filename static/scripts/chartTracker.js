document.addEventListener('DOMContentLoaded', () => {
  const { dates, moodValue, sleepValue, dietValue, energyValue, stressValue } = window.chartData;

  const moodChart = document.getElementById('moodRadarChart').getContext('2d');

  new Chart(moodChart, {
      type: 'line',
      data: {
          labels: dates,
          datasets: [{
              label: 'Mood',
              backgroundColor: 'rgb(255, 99, 132)',
              borderColor: 'rgb(255, 99, 132)',
              data: moodValue,
              tension: 0.2
          },
          {
              label: 'Sleep',
              backgroundColor: 'rgb(55, 160, 245)',
              borderColor: 'rgb(55, 160, 245)',
              data: sleepValue,
              tension: 0.2
          },
          {
              label: 'Diet',
              backgroundColor: 'rgb(255, 165, 0)',
              borderColor: 'rgb(255, 165, 0)',
              data: dietValue,
              tension: 0.2
          },
          {
              label: 'Energy',
              backgroundColor: 'rgb(255, 215, 0)',
              borderColor: 'rgb(255, 215, 0)',
              data: energyValue,
              tension: 0.2
          },
          {
              label: 'Stress',
              backgroundColor: 'rgb(110, 200, 56)',
              borderColor: 'rgb(110, 200, 56)',
              data: stressValue,
              tension: 0.2
          }]
      },
      options: {
          responsiveness: true,
          plugins: {
              title: {
                  display: true,
                  text: 'Mood Tracker Over Time',
                  color: 'black',
                  font: {
                      family: 'Comic Sans MS',
                      size: 32,
                      weight: 'bold'
                  },
                  padding: {top: 10, left: 0, right: 0, bottom: 20}
              },
              legend: {
                  position: 'right'
              }
          },
          scales: {
              x: {
                  display: true,
                  title: {
                      display: true,
                      text: 'Dates',
                      color: 'blue',
                      font: {
                          family: 'Comic Sans MS',
                          size: 22,
                          weight: 'bold'
                      },
                      padding: {top: 10, left: 0, right: 0, bottom: 20}
                  }
              },
              y: {
                  display: true,
                  title: {
                      display: true,
                      text: 'Values',
                      color: 'blue',
                      font: {
                          family: 'Comic Sans MS',
                          size: 22,
                          weight: 'bold'
                      },
                      padding: {top: 10, left: 0, right: 0, bottom: 0}
                  },
                  ticks: {
                      stepSize: 1
                  }
              }
          }
      }
  });
});