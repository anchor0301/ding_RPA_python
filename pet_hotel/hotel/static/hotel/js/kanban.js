let draggedCardId = null;

function handleDragStart(e) {
  draggedCardId = e.target.dataset.id;
}

function allowDrop(e) {
  e.preventDefault();
}

function handleDrop(e) {
  e.preventDefault();

  console.log("🟢 Drop Event Fired!");
  const newStatus = e.currentTarget.dataset.status;

  fetch(`/hotel/reservation/${draggedCardId}/update_status/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({ new_status: newStatus })
  })
  .then(resp => {
    if (resp.ok) {
      location.reload();
    } else {
      alert("상태 변경 실패");
    }
  });
}

