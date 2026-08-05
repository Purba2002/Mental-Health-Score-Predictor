const form = document.getElementById('mh-form');
const statePrompt = document.getElementById('state-prompt');
const stateLoading = document.getElementById('state-loading');
const stateResult = document.getElementById('state-result');
const stateError = document.getElementById('state-error');

const scoreNumber = document.getElementById('score-number');
const scoreContext = document.getElementById('score-context');
const gaugeDot = document.getElementById('gauge-dot');
const errorCopy = document.getElementById('error-copy');
const resetBtn = document.getElementById('reset-btn');
const backBtn = document.getElementById('back-btn');

// Show correct state
function showState(stateToShow) {
  [statePrompt, stateLoading, stateResult, stateError].forEach(s => s.classList.add('hidden'));
  stateToShow.classList.remove('hidden');
}

// 1. STRESS BUTTON LOGIC - Add this after you select form elements
document.querySelectorAll('.stress-buttons button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.stress-buttons button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('stress_level').value = btn.dataset.value;
  });
});

// 2. Animate gauge
function animateGauge(score) {
  const deg = (score / 10) * 180 - 90; // 0-10 maps to -90 to 90 degrees
  gaugeDot.style.transition = 'transform 1s ease-out';
  gaugeDot.style.transform = `rotate(${deg}deg)`;
}

// 3. Get context text based on score
function getBand(score) {
  if (score >= 8) return { label: "Thriving", context: "Your habits point to a well-supported, resilient baseline. Keep it up." };
  if (score >= 6) return { label: "Stable", context: "Mostly good. Watch screen time & sleep to stay balanced." };
  if (score >= 4) return { label: "At Risk", context: "Stress and low activity detected. Try 30min walk + 8hr sleep." };
  return { label: "Low", context: "Consider talking to someone you trust. Small changes can help a lot." };
}

// 4. FORM SUBMIT
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  showState(stateLoading);

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  
  // Convert string numbers to actual numbers
  data.age = parseInt(data.age);
  data.avg_daily_usage_hours = parseFloat(data.avg_daily_usage_hours);
  data.daily_unlocks = parseInt(data.daily_unlocks);
  data.study_hours = parseFloat(data.study_hours);
  data.physical_activity_hours = parseFloat(data.physical_activity_hours);
  data.sleep_hours_per_night = parseFloat(data.sleep_hours_per_night);

  console.log("Sending to backend:", data);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const err = await response.text();
      throw new Error(err);
    }

    const result = await response.json();
    const score = result.predicted_mental_health_score;
    
    scoreNumber.textContent = score.toFixed(1);
    const band = getBand(score);
    scoreContext.textContent = band.context;
    
    animateGauge(score);
    showState(stateResult);

  } catch (err) {
    console.error("Error:", err);
    errorCopy.textContent = "Failed to get prediction. Check if all fields are filled: Age, Gender, Country.";
    showState(stateError);
  }
});

// 5. Reset button
resetBtn.addEventListener('click', () => {
  form.reset();
  document.querySelector('.stress-buttons button[data-value="High"]').classList.add('active');
  document.getElementById('stress_level').value = "High";
  gaugeDot.style.transform = 'rotate(-90deg)';
  showState(statePrompt);
});

// Back button for error
if(backBtn) {
  backBtn.addEventListener('click', () => showState(statePrompt));
}