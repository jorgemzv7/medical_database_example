import uuid
from fastapi import status

def test_create_patient(client, db):
    patient_data = {
        'firstname': 'Jack',
        'lastname': 'Garcia',
        'email': 'jack.garcia@myt.com',
        'contact_record_id': str(uuid.uuid4()),
        'physician_id': str(uuid.uuid4()),
        'medical_condition_id': str(uuid.uuid4())
    }

    response = client.post('/patients/', json=patient_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['email'] == patient_data['email']

def test_get_patient(client, db):
    # Crear paciente primero
    patient_data = {...}  # Igual que arriba
    create_response = client.post('/patients/', json=patient_data)
    patient_id = create_response.json()['patient_id']

    # Obtener paciente
    response = client.get(f'/patients/{patient_id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['patient_id'] == patient_id

def test_update_patient(client, db):
    # Crear paciente
    patient_data = {...}
    create_response = client.post('/patients/', json=patient_data)
    patient_id = create_response.json()['patient_id']

    # Actualizar
    update_data = {'firstname': 'UpdatedName'}
    response = client.put(f'/patients/{patient_id}', json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['firstname'] == 'UpdatedName'

def test_delete_patient(client, db):
    # Crear paciente
    patient_data = {...}
    create_response = client.post('/patients/', json=patient_data)
    patient_id = create_response.json()['patient_id']

    # Borrar (soft-delete)
    response = client.delete(f'/patients/{patient_id}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que está inactivo
    get_response = client.get(f'/patients/{patient_id}')
    assert get_response.json()['is_active'] is False