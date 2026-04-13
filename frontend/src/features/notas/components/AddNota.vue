<script setup>
import { Form, Field } from 'vee-validate'
import { ref, onMounted } from 'vue'
import useToast from '@/stores/useToast'
import BaseButton from '@/components/BaseButton.vue'
import { useAddNota } from '@/features/notas/composables/composables'

const { trigger } = useToast()
const emit = defineEmits(['created'])
const editing = ref({
    id: null,
    field: null,
    value: '',
})

const { sendData: sendAddNota } = useAddNota()

let nombre_nota = ref('')
let observaciones = ref('')

const submit = async () => {
    try {
        await sendAddNota({
            nombre_nota: nombre_nota.value,
            observaciones: observaciones.value,
        })

        nombre_nota.value = ''
        observaciones.value = ''
        emit('create')
    } catch (error) {
        trigger("Nombre nota no debe ser vacío.")
    }
}
</script>

<template>
    <section>
        <!-- Agregar una nota -->
        <div class="grid grid-cols-12">
            <div class="col-span-12">
                <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5 mb-8">
                    <Form @submit="submit()" class="grid grid-cols-1 md:grid-cols-7
                     gap-4 items-end">
                        <div class="form-field md:col-span-2">
                            <div class="pb-3"><label class="form.label">Nombre</label>:</div>

                            <Field type="text" name="nombre_nota" class="form-input" v-model="nombre_nota"
                                placeholder="Ej: Llamar a María" />
                        </div>

                        <div class="form-field md:col-span-4">
                            <div class="pb-3">
                                <label class="form.label">Observaciones</label>
                            </div>

                            <Field type="text" name="observaciones" class="form-input" v-model="observaciones"
                                placeholder="María tiene las llaves de la bodega!" />
                        </div>

                        <BaseButton label="Agregar Personal" type="submit"> Agregar </BaseButton>
                         <div class="form-field col-span-12">
                            
                         </div>
                    </Form>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped></style>
