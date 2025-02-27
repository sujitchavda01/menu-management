$(document).ready(function () {
    loadParentMenus();

    function loadParentMenus() {
        $.ajax({
            url: "/get_menus",
            type: "GET",
            success: function (response) {
                let parentDropdown = $("#parent-id");
                parentDropdown.empty();
                parentDropdown.append('<option value="">Parent (Main Menu)</option>');

                function addOptions(menu, level) {
                    parentDropdown.append(`<option value="${menu.id}">${"➡️".repeat(level)} ${menu.name}</option>`);
                    if (menu.children && menu.children.length > 0) {
                        menu.children.forEach(child => addOptions(child, level + 1));
                    }
                }

                response.forEach(menu => addOptions(menu, 0));
            }
        });
    }

    // Form Submission for Adding Menu
    $("#add-menu-form").submit(function (event) {
        event.preventDefault();
        let menuName = $("#menu-name").val();
        let parentId = $("#parent-id").val();

        $.ajax({
            url: "/add_menu",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ name: menuName, parent_id: parentId }),
            success: function (response) {
                alert(response.success);
                location.reload();
            },
            error: function (xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });

    // Toggle Submenus on Click
    $(document).on("click", ".toggle-btn", function () {
        $(this).siblings("ul").slideToggle();
        $(this).find("i").toggleClass("fa-caret-down fa-caret-right");
    });

    // Delete Menu
    window.deleteMenu = function (id) {
        if (confirm("Are you sure you want to delete this menu?")) {
            $.ajax({
                url: "/delete_menu",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ id: id }),
                success: function (response) {
                    alert(response.success);
                    location.reload();
                },
                error: function (xhr) {
                    alert(xhr.responseJSON.error);
                }
            });
        }
    };

    // Edit Menu
    window.editMenu = function (id, currentName, parentId) {
        let newName = prompt("Edit menu name:", currentName);
        if (newName !== null && newName.trim() !== "") {
            $.ajax({
                url: "/edit_menu",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ id: id, name: newName, parent_id: parentId }),
                success: function (response) {
                    alert(response.success);
                    location.reload();
                },
                error: function (xhr) {
                    alert(xhr.responseJSON.error);
                }
            });
        }
    };
});
