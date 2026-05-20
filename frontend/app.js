const API = "http://localhost:8000";

let state = {
    page: 1,
    query: "",
    products: []
};

// API service for backend communication
const APIService = {
    async getProducts(page = 1, query = "") {
        let url = `${API}/products?page=${page}`;

        if (query) {
            url = `${API}/products/search?q=${query}&page=${page}`;
        }

        const res = await fetch(url);

        if (!res.ok) throw new Error("API error");

        return res.json();
    }
};

// UI controller for rendering and interaction
const UI = {

    async load(page = 1) {
        state.page = page;

        this.showLoading();

        try {
            await new Promise(requestAnimationFrame);

            const data = await APIService.getProducts(page, state.query);

            state.products = data.items;

            this.renderTable(data.items);
            this.renderPagination(data.pagination);

        } catch (err) {
            console.error(err);
            this.showError();
        }
    },

    init() {
        this.load();
    },

    search() {
        state.query = document.getElementById("searchInput").value;
        this.load(1);
    },

    // Show loading state while fetching products
    showLoading() {
        document.getElementById("table-container").innerHTML = `
            <div class="center">
                <div class="spinner"></div>
                <p>Loading products...</p>
            </div>
        `;
    },

    showError() {
        document.getElementById("table-container").innerHTML = `
            <div class="empty-state error">
                <h3>⚠️ Something went wrong</h3>
            </div>
        `;
    },

    // Render products table or empty state
    renderTable(products) {
        const container = document.getElementById("table-container");

        if (!products || products.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No products found</h3>
                    <p>Try another search</p>
                </div>
            `;

            document.getElementById("pagination").innerHTML = "";
            return;
        }

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Rating</th>
                    <th>Stock</th>
                    <th>Brand</th>
                    <th>Category</th>
                    <th>Image</th>
                    <th>Gallery</th>
                </tr>
            </thead>
            <tbody>
        `;

        products.forEach(p => {
            html += `
            <tr id="row-${p.id}">
                <td><strong>${p.title}</strong></td>
                <td class="desc">${p.description}</td>
                <td>$${p.price}</td>
                <td>${p.rating}</td>
                <td>${p.stock}</td>
                <td>${p.brand}</td>
                <td><span class="badge">${p.category}</span></td>
                <td>
                    <img src="${p.thumbnail}" class="thumb">
                </td>
                <td>
                    <button class="btn" onclick="UI.toggleGallery(${p.id})">
                        Gallery
                    </button>
                </td>
            </tr>
            `;
        });

        html += `</tbody></table>`;

        container.innerHTML = html;
    },

    // Toggle product image gallery
    toggleGallery(id) {
        const row = document.getElementById(`row-${id}`);
        const existing = document.getElementById(`gallery-${id}`);

        if (existing) {
            existing.remove();
            return;
        }

        const product = state.products.find(p => p.id === id);
        const images = product?.images || [];

        const galleryRow = document.createElement("tr");
        galleryRow.id = `gallery-${id}`;
        galleryRow.classList.add("gallery-row");

        let html = `<td colspan="9" class="gallery">`;

        images.slice(0, 3).forEach((img, idx) => {
            html += `
            <div class="img-box">

                <div class="spinner small" id="sp-${id}-${idx}"></div>

                <img src="${img}"
                     id="img-${id}-${idx}"
                     onload="UI.onImageLoad(${id}, ${idx})"
                     onerror="UI.onImageError(${id}, ${idx})"
                     style="display:none;" />
            </div>
            `;
        });

        html += `</td>`;

        galleryRow.innerHTML = html;
        row.after(galleryRow);
    },

    onImageLoad(id, idx) {
        document.getElementById(`sp-${id}-${idx}`).style.display = "none";
        document.getElementById(`img-${id}-${idx}`).style.display = "block";
    },

    onImageError(id, idx) {
        const sp = document.getElementById(`sp-${id}-${idx}`);
        if (sp) sp.innerHTML = "❌";
    },

    // Render pagination controls for product pages
    renderPagination(p) {
        const container = document.getElementById("pagination");

        if (!p || p.total_pages === 0) {
            container.innerHTML = "";
            return;
        }

        let html = `<div class="pagination">`;

        html += `
            <button ${!p.has_prev ? "disabled" : ""}
                onclick="UI.load(${p.page - 1})">
                Prev
            </button>
        `;

        html += `<span>Page ${p.page} / ${p.total_pages}</span>`;

        html += `
            <button ${!p.has_next ? "disabled" : ""}
                onclick="UI.load(${p.page + 1})">
                Next
            </button>
        `;

        html += `</div>`;

        container.innerHTML = html;
    }
};

UI.init();