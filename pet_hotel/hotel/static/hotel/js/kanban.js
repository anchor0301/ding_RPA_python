let draggedCardId = null;

function handleDragStart(e) {
  draggedCardId = e.target.dataset.id;
}

function allowDrop(e) {
  e.preventDefault();
}

function handleDrop(e) {
  e.preventDefault();

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
function updateIcon(key, collapsed) {
  const icon = document.getElementById(`icon-${key}`);
  if (icon) icon.textContent = collapsed ? "▶ " : "▼ ";
}

document.addEventListener('DOMContentLoaded', () => {
  const collapsedKey = "kanban_collapsed_columns";
  const collapsed = JSON.parse(localStorage.getItem(collapsedKey) || "[]");

  // 🔁 복원 시 아이콘도 반영
  collapsed.forEach(key => {
    const list = document.getElementById(`column-${key}`);
    if (list) list.classList.add('d-none');
    updateIcon(key, true);
  });

  // 🔁 클릭 시 toggle + 아이콘 + 상태 저장
  document.querySelectorAll('.toggle-header').forEach(header => {
    header.addEventListener('click', () => {
      const key = header.dataset.target;
      const list = document.getElementById(`column-${key}`);
      if (!list) return;

      const isNowCollapsed = list.classList.toggle('d-none');
      updateIcon(key, isNowCollapsed);

      // 저장
      let updated = new Set(collapsed);
      isNowCollapsed ? updated.add(key) : updated.delete(key);
      localStorage.setItem(collapsedKey, JSON.stringify([...updated]));
    });
  });
});
