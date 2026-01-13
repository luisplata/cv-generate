# 🚀 Guía Rápida de Inicio

## Primer Uso

1. **Configurar entorno**
   ```bash
   cp .env.example .env
   nano .env  # O usa tu editor favorito
   ```

2. **Editar master.yaml**
   ```bash
   # Copia el ejemplo
   cp data/master/master.example.yaml data/master/master.yaml
   
   # Edita con tus datos
   nano data/master/master.yaml
   ```

3. **Crear tu primera oferta**
   ```bash
   # Copia el ejemplo simple
   cp data/offers/ejemplo_simple.example.yaml data/offers/Mi_Primera_Oferta.yaml
   
   # Edita según la oferta
   nano data/offers/Mi_Primera_Oferta.yaml
   ```

4. **Generar PDF**
   ```bash
   python generate.py
   ```

5. **Ver resultado**
   ```bash
   # PDF generado en:
   build/Mi_Primera_Oferta/Mi_Primera_Oferta.pdf
   ```

## Checklist para Crear una Oferta

- [ ] Copiar ejemplo: `cp data/offers/ejemplo_simple.example.yaml data/offers/MiOferta.yaml`
- [ ] Editar `profile.title` con el título del puesto
- [ ] Editar `profile.summary` adaptándolo a la oferta
- [ ] Revisar `focus.roles` - deben coincidir con roles en master.yaml
- [ ] Actualizar `focus.skills` con habilidades relevantes
- [ ] Configurar `links` (o dejar que use los del .env)
- [ ] Ajustar `show` según qué secciones mostrar
- [ ] Ejecutar `python generate.py`
- [ ] Revisar PDF en `build/MiOferta/MiOferta.pdf`

## Verificación Rápida

### ¿La experiencia no aparece?
✅ Verifica que `focus.roles` coincida exactamente con `experience[].roles` en master.yaml

### ¿Quiero generar en inglés?
✅ Cambia `.env`: `LANGUAGES=en`
✅ Usa oferta multi-idioma (ejemplo_multilang.yaml)

### ¿Quiero español E inglés?
✅ Cambia `.env`: `LANGUAGES=es,en`
✅ Usa oferta multi-idioma

### ¿Los links no salen?
✅ Define en `.env` O en `links:` del YAML de la oferta
✅ Verifica `show.links: true`

## Comandos Útiles

```bash
# Generar todos los CVs
python generate.py

# Ver archivos generados
ls build/

# Limpiar build anterior
rm -rf build/

# Ver qué ofertas tengo
ls data/offers/

# Ver logs completos (si hay errores)
python generate.py 2>&1 | less
```

## Estructura Mínima de Oferta

```yaml
profile:
  title: "Mi Título"
  summary: "Mi resumen..."

focus:
  roles:
    - Rol1
    - Rol2
  skills:
    - Skill1
    - Skill2

show:
  photo: false
  links: true
  projects: false
  talks: false
  certifications: false
  education: true
```

## Recursos

- README completo: `Readme.md`
- Ejemplo master: `data/master/master.example.yaml`
- Ejemplo simple: `data/offers/ejemplo_simple.example.yaml`
- Ejemplo multi-idioma: `data/offers/ejemplo_multilang.example.yaml`
- Template español: `templates/ats_es.tex`
- Template inglés: `templates/ats_en.tex`
