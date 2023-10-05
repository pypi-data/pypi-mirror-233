def test_single_workflow(rest_client):
    identifier = "myworkflow"

    response = rest_client.get(f"/workflow/{identifier}")
    assert response.status_code == 404

    workflow1a = {"graph": {"id": identifier}, "nodes": [{"id": "task1"}]}
    response = rest_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    workflow1b = {"graph": {"id": identifier}, "nodes": [{"id": "task2"}]}
    response = rest_client.put(f"/workflow/{identifier}", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = rest_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifier": identifier}

    response = rest_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data["message"] == f"Workflow '{identifier}' is not found."

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data["message"] == f"Workflow '{identifier}' is not found."


def test_multiple_workflows(rest_client, default_workflow_identifiers):
    response = rest_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifiers": list(default_workflow_identifiers)}

    workflow1a = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task1"}]}
    workflow1b = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task2"}]}
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": [{"id": "task1"}]}

    response = rest_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.post("/workflows", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 409, data
    assert data["message"] == "Workflow 'myworkflow1' already exists."
    response = rest_client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    expected = default_workflow_identifiers + ["myworkflow1", "myworkflow2"]
    assert sorted(data["identifiers"]) == sorted(expected)


def test_workflow_descriptions(rest_client, default_workflow_identifiers):
    response = rest_client.get("/workflows/descriptions")
    data = response.get_json()
    assert response.status_code == 200
    default_descriptions = [
        desc for desc in data["items"] if desc["id"] in default_workflow_identifiers
    ]
    assert data == {"items": default_descriptions}

    workflow1 = {
        "graph": {"id": "myworkflow1", "label": "label1", "category": "cat1"},
        "nodes": [{"id": "task1"}],
    }
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": [{"id": "task1"}]}
    response = rest_client.post("/workflows", json=workflow1)
    data = response.get_json()
    assert response.status_code == 200, data
    response = rest_client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get("/workflows/descriptions")
    data = response.get_json()["items"]
    assert response.status_code == 200
    expected = default_descriptions + [
        {"id": "myworkflow1", "label": "label1", "category": "cat1"},
        {"id": "myworkflow2"},
    ]
    data = sorted(data, key=lambda x: x["id"])
    assert data == expected


def test_workflow_description_keys(rest_client, default_workflow_identifiers):
    desc = {
        "id": "myworkflow1",
        "label": "label1",
        "category": "cat1",
        "keywords": {"tags": ["XRPD", "ID00"]},
        "input_schema": {"title": "Demo workflow"},
        "ui_schema": {"mx_pipeline_name": {"ui:widget": "checkboxes"}},
    }
    workflow1 = {
        "graph": {
            **desc,
            "custom1": 1,
            "custom2": {},
            "execute_arguments": {"engine": "ppf"},
            "worker_options": {"queue": "id00"},
        },
        "nodes": [{"id": "task1"}],
    }
    response = rest_client.post("/workflows", json=workflow1)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get(
        "/workflows/descriptions", json={"keywords": {"tags": ["XRPD", "ID00"]}}
    )
    data = response.get_json()["items"]
    assert data == [desc], data


def test_workflow_keywords(rest_client, default_workflow_identifiers):
    for instrument_name in ("ID00", "ID99"):
        for scan_type in ("ct", "loopscan"):
            workflow = {
                "graph": {
                    "id": f"myworkflow_{instrument_name}_{scan_type}",
                    "label": "label1",
                    "category": "cat1",
                    "keywords": {
                        "instrument_name": instrument_name,
                        "scan_type": scan_type,
                    },
                },
                "nodes": [{"id": "task1"}],
            }
            response = rest_client.post("/workflows", json=workflow)
            data = response.get_json()
            assert response.status_code == 200, data

    response = rest_client.get("/workflows")
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    expected = default_workflow_identifiers + [
        "myworkflow_ID00_ct",
        "myworkflow_ID00_loopscan",
        "myworkflow_ID99_ct",
        "myworkflow_ID99_loopscan",
    ]
    assert sorted(data) == sorted(expected)

    response = rest_client.get(
        "/workflows", json={"keywords": {"instrument_name": "ID00"}}
    )
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    expected = ["myworkflow_ID00_ct", "myworkflow_ID00_loopscan"]
    assert sorted(data) == sorted(expected)

    response = rest_client.get(
        "/workflows", json={"keywords": {"instrument_name": "ID00", "scan_type": "ct"}}
    )
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    assert data == ["myworkflow_ID00_ct"]

    response = rest_client.get("/workflows/descriptions")
    data = [res["id"] for res in response.get_json()["items"]]
    expected = default_workflow_identifiers + [
        "myworkflow_ID00_ct",
        "myworkflow_ID00_loopscan",
        "myworkflow_ID99_ct",
        "myworkflow_ID99_loopscan",
    ]
    assert sorted(data) == sorted(expected)

    response = rest_client.get(
        "/workflows/descriptions", json={"keywords": {"instrument_name": "ID00"}}
    )
    data = [res["id"] for res in response.get_json()["items"]]
    expected = ["myworkflow_ID00_ct", "myworkflow_ID00_loopscan"]
    assert sorted(data) == sorted(expected)

    response = rest_client.get(
        "/workflows/descriptions",
        json={"keywords": {"instrument_name": "ID00", "scan_type": "ct"}},
    )
    data = [res["id"] for res in response.get_json()["items"]]
    assert data == ["myworkflow_ID00_ct"]
