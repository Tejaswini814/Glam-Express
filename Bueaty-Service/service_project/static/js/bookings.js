function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function triggerReview(bookingId, parlourName) {
  const rating = prompt(`Rate your experience at ${parlourName} (1-5 stars):`);
  if (!rating || isNaN(rating) || rating < 1 || rating > 5) {
    alert("Invalid rating. Please enter a number between 1 and 5.");
    return;
  }

  const review = prompt(`Leave a review for ${parlourName}:`);
  if (!review || review.trim() === "") {
    alert("Review cannot be empty.");
    return;
  }

  // Get CSRF token from cookies (recommended for external files)
  const csrfToken = getCookie("csrftoken");

  fetch(`/booking/${bookingId}/review/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrfToken,
    },
    body: `rating=${rating}&review=${encodeURIComponent(review)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      if (data.status === "success") {
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    });
}
