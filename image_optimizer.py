"""
Module d'optimisation des images uploadées
- Compression automatique
- Redimensionnement
- Conversion en WebP
- Génération de thumbnails
"""

from PIL import Image
import os
from werkzeug.utils import secure_filename


class ImageOptimizer:
    """Classe pour optimiser les images uploadées"""

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_SIZE = (1920, 1920)  # Taille max en pixels
    THUMB_SIZE = (300, 300)  # Taille des miniatures
    QUALITY = 85  # Qualité JPEG/WebP

    @staticmethod
    def allowed_file(filename):
        """Vérifier si l'extension du fichier est autorisée"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImageOptimizer.ALLOWED_EXTENSIONS

    @staticmethod
    def optimize_image(input_path, output_path=None, max_size=None, quality=None):
        """
        Optimiser une image

        Args:
            input_path: Chemin du fichier source
            output_path: Chemin du fichier de sortie (par défaut: écrase l'original)
            max_size: Tuple (width, height) pour redimensionnement
            quality: Qualité de compression (1-100)

        Returns:
            Tuple (success: bool, new_size: int, compression_ratio: float)
        """
        if output_path is None:
            output_path = input_path

        if max_size is None:
            max_size = ImageOptimizer.MAX_SIZE

        if quality is None:
            quality = ImageOptimizer.QUALITY

        try:
            # Ouvrir l'image
            with Image.open(input_path) as img:
                # Taille originale
                original_size = os.path.getsize(input_path)

                # Convertir en RGB si nécessaire (pour JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Créer un fond blanc pour la transparence
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Redimensionner si nécessaire
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Sauvegarder avec compression
                ext = output_path.rsplit('.', 1)[1].lower()

                if ext in ('jpg', 'jpeg'):
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif ext == 'png':
                    img.save(output_path, 'PNG', optimize=True)
                elif ext == 'webp':
                    img.save(output_path, 'WEBP', quality=quality, method=6)
                else:
                    img.save(output_path, quality=quality, optimize=True)

                # Nouvelle taille
                new_size = os.path.getsize(output_path)
                compression_ratio = (1 - new_size / original_size) * 100

                print(f"✅ Image optimisée: {original_size // 1024}KB → {new_size // 1024}KB ({compression_ratio:.1f}% compression)")

                return True, new_size, compression_ratio

        except Exception as e:
            print(f"❌ Erreur optimisation image: {e}")
            return False, 0, 0

    @staticmethod
    def create_thumbnail(input_path, thumb_path, size=None):
        """
        Créer une miniature

        Args:
            input_path: Chemin du fichier source
            thumb_path: Chemin du thumbnail
            size: Tuple (width, height) pour le thumbnail

        Returns:
            bool: True si succès
        """
        if size is None:
            size = ImageOptimizer.THUMB_SIZE

        try:
            with Image.open(input_path) as img:
                # Créer thumbnail (conserve ratio)
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                # Sauvegarder
                img.save(thumb_path, 'JPEG', quality=80, optimize=True)

                print(f"✅ Thumbnail créé: {thumb_path}")
                return True

        except Exception as e:
            print(f"❌ Erreur création thumbnail: {e}")
            return False

    @staticmethod
    def convert_to_webp(input_path, output_path=None, quality=None):
        """
        Convertir une image en WebP (format moderne et performant)

        Args:
            input_path: Chemin du fichier source
            output_path: Chemin du fichier WebP (par défaut: même nom avec .webp)
            quality: Qualité WebP (1-100)

        Returns:
            str: Chemin du fichier WebP créé, ou None si erreur
        """
        if output_path is None:
            base = input_path.rsplit('.', 1)[0]
            output_path = f"{base}.webp"

        if quality is None:
            quality = ImageOptimizer.QUALITY

        try:
            with Image.open(input_path) as img:
                # Convertir en RGB si nécessaire
                if img.mode in ('RGBA', 'LA'):
                    pass  # WebP supporte la transparence
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Sauvegarder en WebP
                img.save(output_path, 'WEBP', quality=quality, method=6)

                original_size = os.path.getsize(input_path)
                webp_size = os.path.getsize(output_path)
                savings = (1 - webp_size / original_size) * 100

                print(f"✅ Converti en WebP: {original_size // 1024}KB → {webp_size // 1024}KB ({savings:.1f}% économie)")

                return output_path

        except Exception as e:
            print(f"❌ Erreur conversion WebP: {e}")
            return None

    @staticmethod
    def batch_optimize(directory, extensions=None, recursive=False):
        """
        Optimiser toutes les images d'un dossier

        Args:
            directory: Chemin du dossier
            extensions: Liste d'extensions à traiter (par défaut: toutes)
            recursive: Traiter les sous-dossiers

        Returns:
            dict: Statistiques (nb_files, total_saved, etc.)
        """
        if extensions is None:
            extensions = ImageOptimizer.ALLOWED_EXTENSIONS

        stats = {
            'nb_files': 0,
            'nb_success': 0,
            'nb_errors': 0,
            'original_size': 0,
            'optimized_size': 0
        }

        # Parcourir le dossier
        for root, dirs, files in os.walk(directory):
            for filename in files:
                ext = filename.rsplit('.', 1)[-1].lower()

                if ext in extensions:
                    filepath = os.path.join(root, filename)
                    original_size = os.path.getsize(filepath)

                    success, new_size, _ = ImageOptimizer.optimize_image(filepath)

                    stats['nb_files'] += 1
                    stats['original_size'] += original_size

                    if success:
                        stats['nb_success'] += 1
                        stats['optimized_size'] += new_size
                    else:
                        stats['nb_errors'] += 1
                        stats['optimized_size'] += original_size

            if not recursive:
                break

        stats['total_saved'] = stats['original_size'] - stats['optimized_size']
        stats['compression_ratio'] = (stats['total_saved'] / stats['original_size'] * 100) if stats['original_size'] > 0 else 0

        return stats


def optimize_uploaded_file(file, upload_folder, create_thumb=True):
    """
    Helper function pour optimiser un fichier uploadé via Flask

    Args:
        file: FileStorage object de Flask
        upload_folder: Dossier de destination
        create_thumb: Créer un thumbnail

    Returns:
        dict: {
            'filename': str,
            'filepath': str,
            'thumb_path': str (optionnel),
            'size': int,
            'optimized': bool
        }
    """
    if not file or not ImageOptimizer.allowed_file(file.filename):
        return None

    # Nom de fichier sécurisé
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)

    # Sauvegarder temporairement
    file.save(filepath)

    # Optimiser
    success, new_size, compression_ratio = ImageOptimizer.optimize_image(filepath)

    result = {
        'filename': filename,
        'filepath': filepath,
        'size': new_size,
        'optimized': success,
        'compression_ratio': compression_ratio
    }

    # Créer thumbnail si demandé
    if create_thumb:
        thumb_name = f"thumb_{filename}"
        thumb_path = os.path.join(upload_folder, thumb_name)

        if ImageOptimizer.create_thumbnail(filepath, thumb_path):
            result['thumb_path'] = thumb_path
            result['thumb_name'] = thumb_name

    return result


if __name__ == '__main__':
    # Test du module
    import sys

    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if os.path.exists(test_file):
            print(f"Test d'optimisation: {test_file}")
            success, size, ratio = ImageOptimizer.optimize_image(test_file)

            if success:
                print(f"✅ Succès! Taille finale: {size // 1024}KB, Compression: {ratio:.1f}%")
            else:
                print("❌ Échec de l'optimisation")
        else:
            print(f"❌ Fichier non trouvé: {test_file}")
    else:
        print("Usage: python image_optimizer.py <fichier_image>")
