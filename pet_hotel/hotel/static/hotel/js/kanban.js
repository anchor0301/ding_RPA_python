const confirmationRules = [
  { from: "checked_in", to: "canceled", message: "🐾 입실 중인 예약을 취소하시겠어요?\n이미 강아지가 입실 중입니다!" },
  { from: "waiting", to: "checked_out", message: "🚪 입실 전 예약을 퇴실 처리하시겠어요?\n아직 입실하지 않았습니다!" },
  { from: "checked_out", to: "waiting", message: "🕐 이미 퇴실한 예약을 다시 입실 전으로 되돌리시겠어요?\n기록이 수정될 수 있어요!" },
  { from: "checked_out", to: "canceled", message: "❗ 퇴실 완료된 예약을 취소로 변경하시겠어요?\n완료된 예약을 되돌리는 행동이에요." },
  { from: "checked_in", to: "waiting", message: "🔄 입실 중인 예약을 입실 전으로 변경하시겠어요?\n방문 기록이 혼동될 수 있어요." }
];

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
  const card = document.getElementById(`card-${draggedCardId}`);
  const targetColumn = document.getElementById(`column-${newStatus}`);
  if (!card || !targetColumn) return;

  const currentStatus = card.dataset.status;
  const rule = confirmationRules.find(rule => rule.from === currentStatus && rule.to === newStatus);
  if (rule && !confirm(rule.message)) return;

  targetColumn.appendChild(card);
  card.dataset.status = newStatus;

  fetch(`/hotel/reservation/${draggedCardId}/update_status/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
    body: JSON.stringify({ new_status: newStatus })
  }).then(resp => {
    if (!resp.ok) {
      alert("상태 변경에 실패했어요 😢 새로고침 후 다시 시도해주세요!");
      location.reload();
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

  // 🔁 칼럼 열림/닫힘 복원
  collapsed.forEach(key => {
    const list = document.getElementById(`column-${key}`);
    if (list) list.classList.add('d-none');
    updateIcon(key, true);
  });

  // 🔁 토글 이벤트
  document.querySelectorAll('.toggle-header').forEach(header => {
    header.addEventListener('click', () => {
      const key = header.dataset.target;
      const list = document.getElementById(`column-${key}`);
      if (!list) return;
      const isNowCollapsed = list.classList.toggle('d-none');
      updateIcon(key, isNowCollapsed);

      let updated = new Set(collapsed);
      isNowCollapsed ? updated.add(key) : updated.delete(key);
      localStorage.setItem(collapsedKey, JSON.stringify([...updated]));
    });
  });

  // 🃏 카드 클릭 시 상세 모달 열기
  document.querySelectorAll('.kanban-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.id;
      fetch(`/hotel/reservation/${id}/detail/`)
        .then(resp => resp.text())
        .then(html => {
          document.getElementById("modalBody").innerHTML = html;
          new bootstrap.Modal(document.getElementById("reservationDetailModal")).show();
        })
        .catch(err => {
          document.getElementById("modalBody").innerHTML = "<p class='text-danger'>불러오기 실패</p>";
        });
    });
  });

  // 🎯 카드 우클릭 컨텍스트 메뉴
  const menu = document.getElementById("cardContextMenu");
  document.querySelectorAll('.kanban-card').forEach(card => {
    card.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      contextMenuCardId = card.dataset.id;
      menu.style.top = `${e.pageY}px`;
      menu.style.left = `${e.pageX}px`;
      menu.classList.remove("d-none");
    });
  });

  menu.querySelectorAll('li').forEach(item => {
    item.addEventListener('click', () => {
      const action = item.dataset.action;
      handleCardAction(contextMenuCardId, action);
      menu.classList.add("d-none");
    });
  });

  document.addEventListener('click', () => {
    menu.classList.add("d-none");
  });

  // 🔄 칼럼별 카드 정렬
  document.querySelectorAll('.kanban-list').forEach(column => {
    const statusKey = column.id.replace("column-", "");
    sortCardsInColumn(column, statusKey);
  });
});
