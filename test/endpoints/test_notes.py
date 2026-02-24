"""
Integration tests for the /api/v1/notes endpoints.

Each test is self-contained: it creates any note it needs via the API and
deletes it on teardown so that tests do not rely on execution order or shared
state.
"""


_NOTE_URL = "/api/v1/notes"


class TestNoteEndpoints:
    """Integration tests for the Notes API."""

    # ------------------------------------------------------------------
    # POST /api/v1/notes/
    # ------------------------------------------------------------------

    def test_create_note(self, client):
        """Creating a note returns 200 with the correct fields."""
        payload = {"title": "Hello", "content": "World"}
        resp = client.post(f"{_NOTE_URL}/", json=payload)

        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["title"] == "Hello"
        assert data["content"] == "World"
        assert isinstance(data["id"], int)
        assert "user" in data

        # Cleanup
        client.delete(f"{_NOTE_URL}/{data['id']}")

    # ------------------------------------------------------------------
    # GET /api/v1/notes/{id}
    # ------------------------------------------------------------------

    def test_get_note(self, client):
        """Fetching a note by its ID returns the correct note."""
        create_resp = client.post(
            f"{_NOTE_URL}/", json={"title": "Get Me", "content": "Retrieve this"}
        )
        note_id = create_resp.json()["id"]

        resp = client.get(f"{_NOTE_URL}/{note_id}")
        assert resp.status_code == 200, resp.text
        assert resp.json()["id"] == note_id
        assert resp.json()["title"] == "Get Me"

        # Cleanup
        client.delete(f"{_NOTE_URL}/{note_id}")

    # ------------------------------------------------------------------
    # PUT /api/v1/notes/{id}
    # ------------------------------------------------------------------

    def test_update_note(self, client):
        """Updating a note title and content is reflected in the response."""
        create_resp = client.post(
            f"{_NOTE_URL}/", json={"title": "Original", "content": "Before"}
        )
        note_id = create_resp.json()["id"]

        resp = client.put(
            f"{_NOTE_URL}/{note_id}",
            json={"title": "Updated", "content": "After"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["title"] == "Updated"
        assert data["content"] == "After"

        # Cleanup
        client.delete(f"{_NOTE_URL}/{note_id}")

    # ------------------------------------------------------------------
    # DELETE /api/v1/notes/{id}
    # ------------------------------------------------------------------

    def test_delete_note(self, client):
        """Deleting a note returns a confirmation and the note is gone."""
        create_resp = client.post(
            f"{_NOTE_URL}/", json={"title": "Bye", "content": "Delete me"}
        )
        note_id = create_resp.json()["id"]

        del_resp = client.delete(f"{_NOTE_URL}/{note_id}")
        assert del_resp.status_code == 200, del_resp.text
        assert del_resp.json()["id_note"] == note_id

        # Confirm note no longer exists (NoteErrorHandler raises 500)
        get_resp = client.get(f"{_NOTE_URL}/{note_id}")
        assert get_resp.status_code in (404, 500)

    # ------------------------------------------------------------------
    # GET /api/v1/notes/list/private
    # ------------------------------------------------------------------

    def test_list_private(self, client):
        """The private list endpoint returns a paginated response structure."""
        create_resp = client.post(
            f"{_NOTE_URL}/", json={"title": "Private", "content": "Mine"}
        )
        note_id = create_resp.json()["id"]

        resp = client.get(f"{_NOTE_URL}/list/private")
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["items"], list)

        # Cleanup
        client.delete(f"{_NOTE_URL}/{note_id}")

    # ------------------------------------------------------------------
    # GET /api/v1/notes/list/public
    # ------------------------------------------------------------------

    def test_list_public(self, client):
        """The public list endpoint returns a paginated response structure."""
        create_resp = client.post(
            f"{_NOTE_URL}/",
            json={"title": "Public", "content": "Visible", "is_public": True},
        )
        note_id = create_resp.json()["id"]

        resp = client.get(f"{_NOTE_URL}/list/public")
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)

        # Cleanup
        client.delete(f"{_NOTE_URL}/{note_id}")
