while True:

    matrix = [

        [j for j in range(100)]

        for i in range(100)

    ]

    result=[

        [

        sum(

        matrix[i][k]

        *

        matrix[k][j]

        for k in range(100)

        )

        for j in range(100)

        ]

        for i in range(100)

    ]