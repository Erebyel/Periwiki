import os
import re
import streamlit as st

# Ruta del directorio 'data' donde se almacenarán los archivos Markdown
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Clase para representar un archivo Markdown
class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.content = self.read()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)

    def replace(self, text, new_text):
        self.content = self.content.replace(text, new_text)

    def save(self):
        self.write(self.content)

    def get_markdown_headers(self):
        return re.findall(r'^#+\s(.+)', self.content, re.MULTILINE)

    def add_header(self, header_text):
        self.content += f"\n\n# {header_text}\n"

    def delete_header(self, header_text):
        self.content = re.sub(rf'^#+\s{re.escape(header_text)}.*?\n', '', self.content, flags=re.MULTILINE)

# Clase para representar un directorio que contiene archivos Markdown
class Directory:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.directories = self.get_subdirectories()
        self.files = self.get_files()

    def get_subdirectories(self):
        return sorted([os.path.join(self.path, d) for d in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, d))])

    def get_files(self):
        files = []
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)) and file.lower().endswith('.md'):
                files.append(File(os.path.join(self.path, file)))
        return sorted(files, key=lambda f: f.name)  # Ordenar los archivos por nombre

    def replace(self, text, new_text):
        for file in self.files:
            file.replace(text, new_text)
            file.save()

    def generate_expander_key(self, file_name):
        return f"{self.name}_{file_name}_expander"

    def generate_radio_key(self, file_name):
        return f"{self.name}_{file_name}_radio"

    def display_files(self):
        for file in self.files:
            expander_key = self.generate_expander_key(file.name)
            with st.expander(str(f"{file.name}"[:-3]).capitalize(), expanded=False):
                radio_key = self.generate_radio_key(file.name)
                col1, col2 = st.columns(2)
                with col1:
                    selected = st.radio(f"", ["Visualizar", "Editar", "Eliminar"], index=0, key=radio_key, horizontal=True, label_visibility= "collapsed")

                if selected == "Eliminar":
                    with col2:
                        # Botón para marcar el archivo para eliminación
                        if st.button("Eliminar", key=os.path.join(self.path, f"{file.name}_delete_button")):
                            os.remove(file.path)
                            st.experimental_rerun()
                            st.warning(f"Se ha eliminado {file.name}")

                if selected == "Visualizar":
                    st.markdown(file.content)
                elif selected == "Editar":
                    edited_content = st.text_area("Modo edición:",file.content)

                    # Botón para guardar cambios
                    if st.button("Guardar cambios", use_container_width=True, key=f"{radio_key}_guardar"):
                        file.write(edited_content)
                        st.success("Cambios guardados")
                        selected = "Visualizar"
                        st.experimental_rerun()
                    else:
                        st.warning("No se han guardado los cambios automáticamente. Recuerda hacer clic en 'Guardar cambios' antes de salir del modo de edición.")

    def display_directory(self, level=0):
        # Mostrar archivos en la carpeta raíz (data)
        root_files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f)) and f.endswith(".md")]
        for file_name in root_files:
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            expander_key = self.generate_expander_key(file_name)
            with st.expander(f"{file.name}", expanded=False):
                radio_key = self.generate_radio_key(file_name)
                col1, col2 = st.columns(2)
                with col1:
                    selected = st.radio(f"", ["Visualizar", "Editar", "Eliminar"], index=0, key=radio_key, horizontal=True, label_visibility= "collapsed")

                if selected == "Eliminar":
                    with col2:
                        # Botón para marcar el archivo para eliminación
                        if st.button("Eliminar", key=os.path.join(DATA_DIR, f"{file.name}_delete_button")):
                            os.remove(file.path)
                            st.experimental_rerun()
                            st.warning(f"Se ha eliminado {file.name}")

                if selected == "Visualizar":
                    st.markdown(file.content)
                elif selected == "Editar":
                    edited_content = st.text_area("Modo edición:",file.content)

                    # Botón para guardar cambios
                    if st.button("Guardar cambios", use_container_width=True, key=f"{radio_key}_guardar"):
                        file.write(edited_content)
                        st.success("Cambios guardados")
                        selected = "Visualizar"
                        st.experimental_rerun()
                    else:
                        st.warning("No se han guardado los cambios automáticamente. Recuerda hacer clic en 'Guardar cambios' antes de salir del modo de edición.")

        # Mostrar directorios y archivos en la carpeta actual
        for subdirectory in self.directories:
            # Formato de los nombres de subdirectorios en mayúscula y negrita
            st.markdown(f"{'#' * (level + 1)} **{os.path.basename(subdirectory).upper()}**")
            subdirectory_obj = Directory(subdirectory)
            subdirectory_obj.display_files()
            # Llamada recursiva para mostrar subdirectorios en niveles inferiores
            subdirectory_obj.display_directory(level + 1)

            # Mostrar directorios y archivos en la carpeta actual
            for subdirectory in self.directories:
                # Formato de los nombres de subdirectorios en mayúscula y negrita
                st.markdown(f"{'#' * (level + 1)} **{os.path.basename(subdirectory).upper()}**")
                subdirectory_obj = Directory(subdirectory)
                subdirectory_obj.display_files()
                # Llamada recursiva para mostrar subdirectorios en niveles inferiores
                subdirectory_obj.display_directory(level + 1)

    def display_subdirectory(self):
        # Mostrar archivos en el subdirectorio actual
        self.display_files()

        # Mostrar directorios y archivos en los subdirectorios
        for subdirectory in self.directories:
            st.markdown(f"{'##' * 2} **{os.path.basename(subdirectory).upper()}**")
            subdirectory_obj = Directory(subdirectory)
            subdirectory_obj.display_subdirectory()

    def get_all_subdirectories(self, parent_prefix=""):
        all_subdirectories = [(parent_prefix + " " + self.name.capitalize(), self.path)]
        for subdirectory in self.directories:
            subdirectory_obj = Directory(subdirectory)
            all_subdirectories.extend(subdirectory_obj.get_all_subdirectories(parent_prefix + "•"))
        return all_subdirectories

    def file_exists(self, file_name):
        for file in self.files:
            if file.name == file_name:
                return True
        return False

def create_file(directory, file_name):
    file_path = os.path.join(directory, f"{file_name}.md")
    with open(file_path, "w") as f:
        f.write("### Nuevo Documento\n")
    st.sidebar.success(f"Se ha creado el nuevo archivo: {file_name}.md")

    # Refrescar la visualización del directorio
    root_directory = Directory(DATA_DIR)
    st.experimental_rerun()  # Vuelve a cargar la aplicación Streamlit

def create_folder(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    os.makedirs(folder_path)
    st.sidebar.success(f"Se ha creado la nueva carpeta: {folder_name}")

    # Refrescar la visualización del directorio
    root_directory = Directory(DATA_DIR)
    st.experimental_rerun()  # Vuelve a cargar la aplicación Streamlit

def delete_folder(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    try:
        os.rmdir(folder_path)
        st.sidebar.success(f"Se ha eliminado la carpeta: {folder_name}")
    except OSError as e:
        st.sidebar.error(f"No se pudo eliminar la carpeta {folder_name}. Asegúrate de que esté vacía.")

    # Refrescar la visualización del directorio
    root_directory = Directory(DATA_DIR)
    st.experimental_rerun()  # Vuelve a cargar la aplicación Streamlit

def search_in_file_names(directory, search_text):
    results = []
    for file in directory.files:
        if search_text.lower() in file.name.lower():
            results.append((file, 0))  # We set matches to 0 since we are searching in file names, not content
    for subdirectory in directory.directories:
        results.extend(search_in_file_names(Directory(subdirectory), search_text))
    return results

def main():
    # Crear la carpeta 'data' si no existe
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Directorio raíz
    root_directory = Directory(DATA_DIR)

    # Inicializar st.session_state
    if "selected_directory_obj" not in st.session_state:
        st.session_state["selected_directory_obj"] = None
    if "selected_search_file" not in st.session_state:
        st.session_state["selected_search_file"] = None

    # CABECERAS
    st.sidebar.title("PeriWiki")
    st.markdown("# Directorio")

    root_directory.display_subdirectory()

    ## CREAR ARCHIVOS Y CARPETAS

    # Opción para elegir si crear un archivo o una carpeta
    st.sidebar.title("Nuevo")
    entry_type = st.sidebar.radio("Selecciona el tipo de entrada:", ["Archivo", "Carpeta"], label_visibility="collapsed")
    new_entry_name = st.sidebar.text_input("Nombre:")

    # Obtener todos los subdirectorios con sangría para representación visual
    all_subdirectories = root_directory.get_all_subdirectories()

    # Mostrar lista de radio con nombres de todos los subdirectorios y la opción "data"
    save_to_dir = st.sidebar.radio("En:", [subdir[0] for subdir in all_subdirectories], index=0)

    if st.sidebar.button("Crear"):
        if new_entry_name:
            # Comprobar si el nombre seleccionado es "data" o un subdirectorio
            if save_to_dir == "data":
                save_to_path = DATA_DIR
            else:
                # Obtener la ruta completa del subdirectorio seleccionado
                selected_subdir_path = next((subdir[1] for subdir in all_subdirectories if subdir[0] == save_to_dir), None)
                if selected_subdir_path:
                    save_to_path = selected_subdir_path
                else:
                    st.sidebar.error("Directorio seleccionado inválido.")
                    return

            # Comprobar si el archivo/carpeta ya existe en el directorio seleccionado
            selected_directory_obj = Directory(save_to_path)
            if entry_type == "Archivo" and selected_directory_obj.file_exists(new_entry_name + ".md"):
                st.sidebar.error("Ya existe un archivo con ese nombre en el directorio seleccionado.")
                return
            elif entry_type == "Carpeta" and os.path.exists(os.path.join(save_to_path, new_entry_name)):
                st.sidebar.error("Ya existe una carpeta con ese nombre en el directorio seleccionado.")
                return

            if entry_type == "Archivo":
                create_file(save_to_path, new_entry_name)
            else:
                create_folder(save_to_path, new_entry_name)
        else:
            st.sidebar.warning("Ingrese un nombre válido para la nueva entrada.")

if __name__ == '__main__':
    main()
