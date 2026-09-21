import fitz

fn = r'Three.js For Beginners An In-depth Guide to 3D Graphics and Animations for Modern Websites (Jiho Seok).pdf'
doc=fitz.open(fn)
doc.set_toc([])
toc = [[1, 'Contents', 9],
       [1,'1.Introduction to 3D Web Graphics and Three.js',23],
       [1,'2.Diving Deep into Three.js Fundamentals',49],
       [1,'3.Exploring the 3D World with Three.js',137],
       [1,'4.Tween.js for Animation in Three.js',154],
       [1,'5.Mathematics and Physics in Three.js',178]]
doc.set_toc(toc)
doc.saveIncr()

