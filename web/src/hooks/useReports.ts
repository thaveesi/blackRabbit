import { useEffect, useState } from "react"
import { AttackReport } from "../types"
import { BASE_API_URL } from "../constants"

export const useGetReports = () => {
    const [reports, setReports] = useState<AttackReport[]>([])
    useEffect(() => {
        fetch(`${BASE_API_URL}/reports`, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(res => res.json())
        .then(data => setReports(data))
    }, [])

    return reports
}