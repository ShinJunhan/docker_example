// ================= [ Member CRUD ] =================

// 1. 조회 (READ)
async function fetchMembers() {
    const listDiv = document.getElementById('member-list');
    try {
        const res = await fetch('/members');
        const json = await res.json();
        listDiv.innerHTML = json.data.map(m => `
            <div class="item">
                <span><strong>${m.num}. ${m.name}</strong> (${m.addr})</span>
                <div class="btn-group">
                    <button onclick="updateMember(${m.num}, '${m.name}', '${m.addr}')" class="btn-edit">수정</button>
                    <button onclick="deleteMember(${m.num})" class="btn-del">삭제</button>
                </div>
            </div>
        `).join('') || "데이터가 없습니다.";
    } catch (e) { listDiv.innerHTML = "조회 실패"; }
}

// 2. 등록 (CREATE)
async function saveMember() {
    const name = document.getElementById('member-name').value;
    const addr = document.getElementById('member-addr').value;
    if(!name || !addr) return alert("내용을 입력하세요.");

    await fetch('/members', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, addr })
    });
    location.reload(); // 단순하게 전체 갱신
}

// 3. 수정 (UPDATE)
async function updateMember(num, oldName, oldAddr) {
    const newName = prompt("수정할 이름을 입력하세요", oldName);
    const newAddr = prompt("수정할 주소를 입력하세요", oldAddr);
    if (!newName || !newAddr) return;

    await fetch(`/members/${num}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName, addr: newAddr })
    });
    fetchMembers();
}

// 4. 삭제 (DELETE)
async function deleteMember(num) {
    if (!confirm("정말 삭제하시겠습니까?")) return;
    await fetch(`/members/${num}`, { method: 'DELETE' });
    fetchMembers();
}

// ================= [ Post CRUD ] =================

async function fetchPosts() {
    const listDiv = document.getElementById('post-list');
    try {
        const res = await fetch('/posts');
        const json = await res.json();
        listDiv.innerHTML = json.data.map(p => `
            <div class="item">
                <span><strong>${p.num}. ${p.title}</strong> (by ${p.writer})</span>
                <div class="btn-group">
                    <button onclick="updatePost(${p.num}, '${p.writer}', '${p.title}')" class="btn-edit">수정</button>
                    <button onclick="deletePost(${p.num})" class="btn-del">삭제</button>
                </div>
            </div>
        `).join('') || "게시글이 없습니다.";
    } catch (e) { listDiv.innerHTML = "조회 실패"; }
}

async function savePost() {
    const writer = document.getElementById('post-writer').value;
    const title = document.getElementById('post-title').value;
    if(!writer || !title) return alert("내용을 입력하세요.");

    await fetch('/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ writer, title })
    });
    location.reload();
}

async function updatePost(num, oldWriter, oldTitle) {
    const newWriter = prompt("수정할 작성자", oldWriter);
    const newTitle = prompt("수정할 제목", oldTitle);
    if (!newWriter || !newTitle) return;

    await fetch(`/posts/${num}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ writer: newWriter, title: newTitle })
    });
    fetchPosts();
}

async function deletePost(num) {
    if (!confirm("정말 삭제하시겠습니까?")) return;
    await fetch(`/posts/${num}`, { method: 'DELETE' });
    fetchPosts();
}

window.onload = () => { fetchMembers(); fetchPosts(); };