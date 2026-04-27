<script setup>
import { ref, onMounted } from 'vue'

const API = 'http://localhost:8000'

const tesis = ref([])
const avances = ref([])
const actual = ref(null)

const nueva = ref({
  titulo: '',
  estudiante: '',
  director: '',
  linea_investigacion: '',
  estado: 'en proceso'
})

const avance = ref({
  descripcion: '',
  porcentaje_avance: 0,
  observaciones: ''
})

async function cargar() {
  const r = await fetch(`${API}/tesis`)
  tesis.value = await r.json()
}

async function guardar() {
  await fetch(`${API}/tesis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(nueva.value)
  })

  nueva.value = {
    titulo: '',
    estudiante: '',
    director: '',
    linea_investigacion: '',
    estado: 'en proceso'
  }

  cargar()
}

async function ver(t) {
  actual.value = t
  const r = await fetch(`${API}/tesis/${t.id}/avances`)
  avances.value = await r.json()
}

async function guardarAvance() {
  await fetch(`${API}/tesis/${actual.value.id}/avances`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(avance.value)
  })

  avance.value = {
    descripcion: '',
    porcentaje_avance: 0,
    observaciones: ''
  }

  ver(actual.value)
}

onMounted(cargar)
</script>

<template>
  <div class="container py-4">

    <!-- HEADER -->
    <div class="mb-4">
      <h1 class="fw-bold">Gestión de Tesis</h1>
      <p class="text-muted">Registro y seguimiento de avances académicos</p>
    </div>

    <!-- FORMULARIO -->
    <div class="card mb-4">
      <div class="card-header fw-bold">
        Nueva tesis
      </div>

      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-6">
            <input v-model="nueva.titulo" class="form-control" placeholder="Título">
          </div>

          <div class="col-md-6">
            <input v-model="nueva.estudiante" class="form-control" placeholder="Estudiante">
          </div>

          <div class="col-md-6">
            <input v-model="nueva.director" class="form-control" placeholder="Director">
          </div>

          <div class="col-md-6">
            <input v-model="nueva.linea_investigacion" class="form-control" placeholder="Línea">
          </div>

          <div class="col-md-4">
            <select v-model="nueva.estado" class="form-select">
              <option>pendiente</option>
              <option>en proceso</option>
              <option>revisada</option>
            </select>
          </div>
        </div>

        <button class="btn btn-primary mt-3" @click="guardar">
          Guardar tesis
        </button>
      </div>
    </div>

    <!-- CONTENIDO -->
    <div class="row">

      <!-- LISTA TESIS -->
      <div class="col-lg-7">
        <h4 class="mb-3">Tesis registradas</h4>

        <div v-for="t in tesis" :key="t.id" class="card mb-3">
          <div class="card-body">

            <div class="d-flex justify-content-between align-items-start">
              <h5 class="card-title">{{ t.titulo }}</h5>
              <span class="badge bg-primary">{{ t.estado }}</span>
            </div>

            <p class="mb-1"><strong>Estudiante:</strong> {{ t.estudiante }}</p>
            <p class="mb-1"><strong>Director:</strong> {{ t.director }}</p>
            <p class="mb-2"><strong>Línea:</strong> {{ t.linea_investigacion }}</p>

            <button class="btn btn-outline-primary btn-sm" @click="ver(t)">
              Ver avances
            </button>

          </div>
        </div>
      </div>

      <!-- AVANCES -->
      <div class="col-lg-5">

        <div v-if="actual" class="card">
          <div class="card-header">
            Avances
          </div>

          <div class="card-body">
            <h5>{{ actual.titulo }}</h5>
            <p class="text-muted">Estudiante: {{ actual.estudiante }}</p>

            <!-- FORM AVANCE -->
            <div class="mb-3">
              <input v-model="avance.descripcion" class="form-control mb-2" placeholder="Descripción">

              <input
                v-model="avance.porcentaje_avance"
                type="number"
                class="form-control mb-2"
                placeholder="Porcentaje"
              >

              <input v-model="avance.observaciones" class="form-control mb-2" placeholder="Observaciones">

              <button class="btn btn-success w-100" @click="guardarAvance">
                Guardar avance
              </button>
            </div>

            <!-- LISTA AVANCES -->
            <div v-if="avances.length === 0" class="alert alert-warning">
              Sin avances registrados
            </div>

            <div v-for="a in avances" :key="a.id" class="border rounded p-3 mb-3">

              <div class="d-flex justify-content-between">
                <strong>{{ a.porcentaje_avance }}%</strong>
                <small class="text-muted">{{ a.fecha }}</small>
              </div>

              <div class="progress my-2">
                <div
                  class="progress-bar"
                  role="progressbar"
                  :style="{ width: a.porcentaje_avance + '%' }"
                >
                  {{ a.porcentaje_avance }}%
                </div>
              </div>

              <p class="mb-1">{{ a.descripcion }}</p>
              <small class="text-muted">{{ a.observaciones }}</small>

            </div>
          </div>
        </div>

        <div v-else class="alert alert-info">
          Seleccione una tesis para ver sus avances
        </div>

      </div>
    </div>

  </div>
</template>
